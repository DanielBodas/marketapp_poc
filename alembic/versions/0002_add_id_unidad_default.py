"""
Revision ID: 0002_add_id_unidad_default
Revises: 0001_init
Create Date: 2025-10-16
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Añadir columna id_unidad a compras con valor por defecto 1
    op.add_column('compras', sa.Column('id_unidad', sa.Integer(), nullable=False, server_default='1'))
    # Opcional: actualizar registros existentes si necesitas otro valor
    # op.execute("UPDATE compras SET id_unidad = <otro_id> WHERE <condicion>")
    # Quitar el valor por defecto para futuras inserciones
    op.alter_column('compras', 'id_unidad', server_default=None)

def downgrade():
    op.drop_column('compras', 'id_unidad')
