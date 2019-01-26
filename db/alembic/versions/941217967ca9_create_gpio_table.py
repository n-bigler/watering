"""create_gpio_table

Revision ID: 941217967ca9
Revises: 69a9b2a8a1f9
Create Date: 2019-01-26 20:13:35.958843

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '941217967ca9'
down_revision = '69a9b2a8a1f9'
branch_labels = None
depends_on = None


def upgrade():
	op.add_column('gpio', sa.Column('type', sa.String(50), nullable=False, server_default="valve"))
	op.add_column('gpio', sa.Column('group', sa.Integer, nullable=False, server_default="1"))


def downgrade():
	op.drop_column('gpio', 'type')
	op.drop_column('gpio', 'group')
