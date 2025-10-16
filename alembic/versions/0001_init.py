"""
Revision ID: 0001_init
Revises: 
Create Date: 2025-10-16

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # ejemplo: crear tabla compras
    op.create_table(
        'compras',
        sa.Column('id_compra', sa.Integer, primary_key=True),
        sa.Column('fecha', sa.Date, nullable=False),
        sa.Column('id_supermercado', sa.Integer, nullable=False),
        sa.Column('id_producto', sa.Integer, nullable=False),
        sa.Column('id_marca', sa.Integer, nullable=False),
        sa.Column('id_unidad', sa.Integer, nullable=False),
        sa.Column('precio', sa.Float, nullable=False),
        sa.Column('cantidad', sa.Integer, nullable=False)
    )
    # ...añadir más tablas según modelos

def downgrade():
    op.drop_table('compras')
    # ...eliminar más tablas si es necesario
