"""default for placed_at

Revision ID: f9046868fb5e
Revises: f60a9cf48d34
Create Date: 2016-11-21 14:40:23.086880

"""

# revision identifiers, used by Alembic.
revision = 'f9046868fb5e'
down_revision = 'f60a9cf48d34'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column('placements', 'placed_at', server_default=sa.func.now())


def downgrade():
    op.alter_column('placements', 'placed_at', server_default=None)
