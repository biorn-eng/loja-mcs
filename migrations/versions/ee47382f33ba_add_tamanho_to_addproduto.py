"""Add tamanho to Addproduto

Revision ID: ee47382f33ba
Revises: 038a49f1e8c1
Create Date: 2024-08-16 18:50:35.141565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee47382f33ba'
down_revision = '038a49f1e8c1'
branch_labels = None
depends_on = None


def upgrade():
    # Adiciona a coluna 'tamanho' com um valor padrão 'M'
    with op.batch_alter_table('addproduto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tamanho', sa.String(length=50), nullable=False, server_default='M'))

    # ### end Alembic commands ###


def downgrade():
    # Remove a coluna 'tamanho'
    with op.batch_alter_table('addproduto', schema=None) as batch_op:
        batch_op.drop_column('tamanho')

    # ### end Alembic commands ###
