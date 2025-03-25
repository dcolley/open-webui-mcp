"""add mcp_server table

Revision ID: e22ecd25e4f7
Revises: 3781e22d8b01
Create Date: 2025-03-13 18:01:15.826784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import open_webui.internal.db
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision: str = 'e22ecd25e4f7'
down_revision: Union[str, None] = '3781e22d8b01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
        sa.Column('valves', sa.TEXT(), nullable=True),
        sa.Column('enabled', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Add indexes
    op.create_index('ix_mcp_server_name', 'mcp_server', ['name'], unique=True)
    op.create_index('ix_mcp_server_user_id', 'mcp_server', ['user_id'])
    op.create_index('ix_mcp_server_url', 'mcp_server', ['url'], unique=True)
    op.create_index('ix_mcp_server_enabled', 'mcp_server', ['enabled'])


def downgrade() -> None:
    op.drop_index('ix_mcp_server_name')
    op.drop_index('ix_mcp_server_url')
    op.drop_index('ix_mcp_server_enabled')

    # Drop table
    op.drop_table('mcp_server') 
