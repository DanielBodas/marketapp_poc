"""Tests para la lógica de negocio del formulario de compras"""
import pytest
from db.models import Producto, Marca, Unidad, ProductoMarca, ProductoUnidad
from domain.compra import get_marcas_para_producto, get_unidad_para_producto

@pytest.fixture
def sample_data():
    # Productos de prueba
    p1 = Producto(id_producto=1, nombre_producto="Leche")
    p2 = Producto(id_producto=2, nombre_producto="Pan")
    
    # Marcas de prueba
    m1 = Marca(id_marca=1, nombre_marca="Marca1")
    m2 = Marca(id_marca=2, nombre_marca="Marca2")
    
    # Unidades de prueba
    u1 = Unidad(id_unidad=1, nombre_unidad="unidad")
    u2 = Unidad(id_unidad=2, nombre_unidad="litro")
    
    # Relaciones producto-marca
    pm1 = ProductoMarca(id_producto_marca=1, id_producto=1, id_marca=1)  # Leche-Marca1
    pm2 = ProductoMarca(id_producto_marca=2, id_producto=1, id_marca=2)  # Leche-Marca2
    pm3 = ProductoMarca(id_producto_marca=3, id_producto=2, id_marca=1)  # Pan-Marca1
    
    # Relaciones producto-unidad
    pu1 = ProductoUnidad(id_producto_unidad=1, id_producto=1, id_unidad=2)  # Leche-litro
    pu2 = ProductoUnidad(id_producto_unidad=2, id_producto=2, id_unidad=1)  # Pan-unidad
    
    return {
        "productos": [p1, p2],
        "marcas": [m1, m2],
        "unidades": [u1, u2],
        "relaciones_pm": [pm1, pm2, pm3],
        "relaciones_pu": [pu1, pu2]
    }


def test_get_marcas_para_producto(sample_data):
    """Test para verificar que se obtienen las marcas correctas para un producto"""
    producto = sample_data["productos"][0]  # Leche
    marcas = get_marcas_para_producto(
        producto.id_producto,
        sample_data["relaciones_pm"],
        sample_data["marcas"]
    )
    
    # La leche debe tener dos marcas disponibles
    assert len(marcas) == 2
    assert all(m.id_marca in [1, 2] for m in marcas)

def test_get_marcas_producto_none(sample_data):
    """Test para verificar que se obtiene lista vacía si no hay producto seleccionado"""
    marcas = get_marcas_para_producto(
        None,
        sample_data["relaciones_pm"],
        sample_data["marcas"]
    )
    assert len(marcas) == 0

def test_get_unidad_para_producto(sample_data):
    """Test para verificar que se obtiene la unidad correcta para un producto"""
    producto = sample_data["productos"][0]  # Leche
    unidad = get_unidad_para_producto(
        producto.id_producto,
        sample_data["relaciones_pu"],
        sample_data["unidades"]
    )
    
    # La leche debe tener "litro" como unidad
    assert unidad.nombre_unidad == "litro"

def test_get_unidad_por_defecto(sample_data):
    """Test para verificar que se obtiene 'unidad' por defecto"""
    producto = sample_data["productos"][1]  # Pan
    unidad = get_unidad_para_producto(
        producto.id_producto,
        sample_data["relaciones_pu"],
        sample_data["unidades"]
    )
    
    # El pan debe tener "unidad" como unidad por defecto
    assert unidad.nombre_unidad == "unidad"

def test_get_unidad_producto_none(sample_data):
    """Test para verificar que se obtiene None si no hay producto seleccionado"""
    unidad = get_unidad_para_producto(
        None,
        sample_data["relaciones_pu"],
        sample_data["unidades"]
    )
    assert unidad is None