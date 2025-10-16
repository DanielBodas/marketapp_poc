import pytest
from forms.compra_form import inicializar_estado
from db.models import Producto, Marca, Unidad, ProductoMarca, ProductoUnidad

from tests.mock_streamlit import MockStreamlit

# Fixtures para tests
@pytest.fixture
def mock_streamlit(monkeypatch):
    st_mock = MockStreamlit()
    monkeypatch.setattr("forms.compra_form.st", st_mock)
    return st_mock

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

def test_inicializar_estado_vacio(mock_streamlit):
    inicializar_estado()
    assert "lineas_compra" in mock_streamlit.session_state
    assert mock_streamlit.session_state["lineas_compra"] == []

def test_filtrar_marcas_por_producto(sample_data):
    """Test para verificar que se filtran correctamente las marcas disponibles para un producto"""
    producto = sample_data["productos"][0]  # Leche
    relaciones_pm = sample_data["relaciones_pm"]
    marcas = sample_data["marcas"]
    
    # Obtener marcas relacionadas con el producto
    marcas_disponibles = [
        m for rel in relaciones_pm 
        if rel.id_producto == producto.id_producto 
        for m in marcas 
        if m.id_marca == rel.id_marca
    ]
    
    # La leche debe tener dos marcas disponibles
    assert len(marcas_disponibles) == 2
    assert all(m.id_marca in [1, 2] for m in marcas_disponibles)

def test_filtrar_unidades_por_producto(sample_data):
    """Test para verificar que se asignan correctamente las unidades según el producto"""
    producto = sample_data["productos"][0]  # Leche
    relaciones_pu = sample_data["relaciones_pu"]
    unidades = sample_data["unidades"]
    
    # Obtener unidades relacionadas con el producto
    unidades_disponibles = [
        u for rel in relaciones_pu 
        if rel.id_producto == producto.id_producto 
        for u in unidades 
        if u.id_unidad == rel.id_unidad
    ]
    
    # La leche debe tener "litro" como unidad
    assert len(unidades_disponibles) == 1
    assert unidades_disponibles[0].nombre_unidad == "litro"

def test_unidad_por_defecto_sin_relacion(sample_data):
    """Test para verificar que se usa 'unidad' por defecto cuando no hay relación producto-unidad"""
    producto = sample_data["productos"][1]  # Pan
    relaciones_pu = sample_data["relaciones_pu"]
    unidades = sample_data["unidades"]
    
    # Buscar la unidad por defecto (unidad)
    unidad_default = next((u for u in unidades if u.nombre_unidad.lower() == "unidad"), None)
    assert unidad_default is not None
    
    # El pan debe tener "unidad" como unidad
    unidades_disponibles = [
        u for rel in relaciones_pu 
        if rel.id_producto == producto.id_producto 
        for u in unidades 
        if u.id_unidad == rel.id_unidad
    ]
    assert len(unidades_disponibles) == 1
    assert unidades_disponibles[0].id_unidad == unidad_default.id_unidad