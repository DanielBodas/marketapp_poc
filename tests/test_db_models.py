import pytest
from db import models


def test_models_have_tables():
    # Comprueba que las clases de modelo están definidas y tienen __tablename__
    assert hasattr(models, "Producto")
    assert hasattr(models.Producto, "__tablename__")
    assert hasattr(models, "Marca")
    assert hasattr(models.Marca, "__tablename__")
    assert hasattr(models, "Supermercado")
    assert hasattr(models.Supermercado, "__tablename__")
    assert hasattr(models, "Compra")
    assert hasattr(models.Compra, "__tablename__")


def test_producto_fields():
    # Comprueba algunos campos de Producto
    Producto = models.Producto
    assert hasattr(Producto, "id_producto")
    assert hasattr(Producto, "nombre_producto")
