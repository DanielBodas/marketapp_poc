from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Date, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# ---- CLASIFICACIÓN ----
class Clasificacion(Base):
    """Tabla de clasificaciones de productos."""
    __tablename__ = "clasificaciones"

    id_clasificacion = Column(Integer, primary_key=True)
    nombre_clasificacion = Column(String, unique=True, nullable=False)


# ---- MARCA ----
class Marca(Base):
    """Tabla de marcas."""
    __tablename__ = "marcas"

    id_marca = Column(Integer, primary_key=True)
    nombre_marca = Column(String, unique=True, nullable=False)


# ---- PRODUCTO ----
class Producto(Base):
    """Tabla de productos."""
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True)
    nombre_producto = Column(String, unique=True, nullable=False)


# ---- SUPERMERCADO ----
class Supermercado(Base):
    """Tabla de supermercados."""
    __tablename__ = "supermercados"

    id_supermercado = Column(Integer, primary_key=True)
    nombre_supermercado = Column(String, unique=True, nullable=False)


# ---- RELACIÓN PRODUCTO ↔ MARCA ----
class ProductoMarca(Base):
    """
    Tabla intermedia que relaciona productos con marcas.
    """
    __tablename__ = "productos_marcas"

    id_producto_marca = Column(Integer, primary_key=True)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_marca = Column(Integer, ForeignKey("marcas.id_marca"), nullable=False)

    __table_args__ = (
        UniqueConstraint("id_producto", "id_marca", name="uq_producto_marca"),
    )

# ---- COMPRA ----
class Compra(Base):
    """Tabla de compras realizadas."""
    __tablename__ = "compras"

    id_compra = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)

    id_supermercado = Column(Integer, ForeignKey("supermercados.id_supermercado"), nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id_producto"), nullable=False)
    id_marca = Column(Integer, ForeignKey("marcas.id_marca"), nullable=False)

    precio = Column(Float, nullable=False)
    cantidad = Column(Integer, nullable=False)
