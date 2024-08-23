"""Adicionando modelo de avaliações

Revision ID: 3ab48964eef8
Revises: 92a22449cc27
Create Date: 2024-08-16 01:01:07.381466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ab48964eef8'
down_revision = '92a22449cc27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('avaliacao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('produto_id', sa.Integer(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.Column('comentario', sa.Text(), nullable=False),
    sa.Column('estrelas', sa.Integer(), nullable=False),
    sa.Column('data_criado', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['produto_id'], ['addproduto.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('avaliacao')
    # ### end Alembic commands ###
