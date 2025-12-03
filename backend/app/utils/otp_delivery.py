import logging

logger = logging.getLogger("otp")

def send_sms_otp(phone: str, otp: str):
    logger.info(f"[SMS OTP] {phone}: {otp}")

def send_email_otp(email: str, otp: str):
    logger.info(f"[EMAIL OTP] {email}: {otp}")
