"""create_gpio_table

Revision ID: 69a9b2a8a1f9
Revises: 
Create Date: 2019-01-23 15:52:16.589812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69a9b2a8a1f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    	'gpio',
    	sa.Column('id', sa.Integer, primary_key=True),
    	sa.Column('name', sa.String(50), nullable=False),
    	sa.Column('description', sa.Unicode(200)),
    	)


def downgrade():
	op.drop_table('gpio');

