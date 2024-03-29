"""Database

Revision ID: 4fdfca6cf7a4
Revises:
Create Date: 2024-01-22 22:48:07.524416

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4fdfca6cf7a4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('submenu',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('menu_id', sa.UUID(), nullable=True),
                    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('dish',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('price', sa.Float(), nullable=True),
                    sa.Column('submenu_id', sa.UUID(), nullable=True),
                    sa.ForeignKeyConstraint(['submenu_id'], ['submenu.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dish')
    op.drop_table('submenu')
    op.drop_table('menu')
    # ### end Alembic commands ###
