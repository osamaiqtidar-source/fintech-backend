from .celery_app import celery_app
from .db import get_session
from .models import Subscription, User
from sqlmodel import select
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage

def send_email(to_email, subject, body):
    host = os.getenv('SMTP_HOST')
    port = int(os.getenv('SMTP_PORT', '587'))
    user = os.getenv('SMTP_USER')
    pwd = os.getenv('SMTP_PASS')
    if not host or not user or not pwd:
        print('SMTP not configured; skipping email to', to_email)
        return False
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = to_email
    msg.set_content(body)
    try:
        with smtplib.SMTP(host, port) as s:
            s.starttls()
            s.login(user, pwd)
            s.send_message(msg)
        return True
    except Exception as e:
        print('Failed to send email', e)
        return False

@celery_app.task
def send_reminder_task(subscription_id: int, email: str, days_left: int):
    subject = f'Subscription expiring in {days_left} days'
    body = f'Your subscription (id: {subscription_id}) will expire in {days_left} days. Please renew.'
    ok = send_email(email, subject, body)
    # optionally log in subscription_reminders table
    session = get_session()
    sr = {'subscription_id': subscription_id, 'method': 'email', 'status': 'sent' if ok else 'failed', 'message': None}
    try:
        session.execute("""INSERT INTO subscription_reminders (subscription_id, method, status, message) VALUES (:subscription_id, :method, :status, :message)""", sr)
        session.commit()
    except Exception as e:
        print('Failed to log reminder', e)

def check_and_schedule_reminders():
    session = get_session()
    subs = session.exec(select(Subscription).where(Subscription.status == 'active')).all()
    now = datetime.utcnow()
    for s in subs:
        if s.end_date:
            days = (s.end_date - now).days
            if days in (7,3,1):
                # find an email to send: choose first user of company
                user = session.exec(select(User).where(User.company_id == s.company_id)).first()
                if user:
                    send_reminder_task.delay(s.id, user.email, days)

def schedule_periodic_tasks():
    # called at startup in main; also can be run in worker via beat if configured
    from apscheduler.schedulers.background import BackgroundScheduler
    sched = BackgroundScheduler()
    sched.add_job(check_and_schedule_reminders, 'interval', hours=24)
    sched.start()
