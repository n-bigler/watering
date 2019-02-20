"""create_processes_table

Revision ID: 9bbb77b3235f
Revises: 941217967ca9
Create Date: 2019-02-20 20:35:06.563852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bbb77b3235f'
down_revision = '941217967ca9'
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'process',
		sa.Column('name', sa.String(200), primary_key=True),
		sa.Column('description', sa.String(200), nullable=False, server_default="no description"),
		sa.Column('filename', sa.String(200), nullable=False))


def downgrade():
	op.drop_table('gpio')
