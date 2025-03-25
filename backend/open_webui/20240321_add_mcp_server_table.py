"""add mcp server table

Revision ID: 20240321_add_mcp_server_table
Revises: 20240320_add_license_metadata
Create Date: 2024-03-21 00:00:00.000000

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision = '20240321'
down_revision = 'ca81bd47c050'
branch_labels = Union[str, Sequence[str], None] = None
depends_on = Union[str, Sequence[str], None] = None


def upgrade():
    # Create mcp_server table
    op.create_table(
        'mcp_server',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        # type: command or url
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('command', sa.String(), nullable=True),
        sa.Column('url', sa.String(), nullable=True),
        # sa.Column('api_key', sa.String(), nullable=True),
        # valves
        sa.Column('valves', sa.JSON(), nullable=True),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Add indexes
    op.create_index('ix_mcp_server_name', 'mcp_server', ['name'], unique=True)
    op.create_index('ix_mcp_server_user_id', 'mcp_server', ['user_id'])
    op.create_index('ix_mcp_server_url', 'mcp_server', ['url'], unique=True)
    op.create_index('ix_mcp_server_enabled', 'mcp_server', ['enabled'])


def downgrade():
    # Drop indexes
    op.drop_index('ix_mcp_server_name')
    op.drop_index('ix_mcp_server_url')
    op.drop_index('ix_mcp_server_enabled')

    # Drop table
    op.drop_table('mcp_server') 