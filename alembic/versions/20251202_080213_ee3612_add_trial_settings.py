"""add trialsettings table and company fields

Revision ID: 20251202_080213_ee3612
Revises: 
Create Date: 2025-12-02T08:02:13.025412
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20251202_080213_ee3612'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create trialsettings table
    op.create_table(
        'trialsettings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('trial_enabled', sa.Boolean, nullable=False, server_default=sa.text('true')),
        sa.Column('trial_days', sa.Integer, nullable=False, server_default='14'),
        sa.Column('feature_flags', sa.JSON, nullable=True),
        sa.Column('updated_by', sa.Integer, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
    )
    # Add columns to companies table
    with op.batch_alter_table('companies') as batch_op:
        batch_op.add_column(sa.Column('has_trial_once', sa.Boolean, nullable=False, server_default=sa.text('false')))
        batch_op.add_column(sa.Column('trial_started_at', sa.DateTime, nullable=True))
        batch_op.add_column(sa.Column('trial_ended_at', sa.DateTime, nullable=True))

def downgrade():
    with op.batch_alter_table('companies') as batch_op:
        batch_op.drop_column('trial_ended_at')
        batch_op.drop_column('trial_started_at')
        batch_op.drop_column('has_trial_once')
    op.drop_table('trialsettings')
