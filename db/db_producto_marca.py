from db.connection import get_session, session_scope
from db.models import ProductoMarca
from sqlalchemy.exc import IntegrityError

def obtener_relaciones_producto_marca():
    session = get_session()
    return session.query(ProductoMarca).all()

def insertar_relacion_producto_marca(id_producto: int, id_marca: int):
    nueva = ProductoMarca(id_producto=id_producto, id_marca=id_marca)
    try:
        with session_scope() as session:
            session.add(nueva)
        return True, "Relación producto-marca creada."
    except IntegrityError:
        return False, "La relación ya existe."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"

def eliminar_relacion_producto_marca(id_producto_marca: int):
    try:
        with session_scope() as session:
            relacion = session.get(ProductoMarca, id_producto_marca)
            if not relacion:
                return False, "Relación no encontrada."
            session.delete(relacion)
        return True, "Relación eliminada."
    except Exception as e:
        return False, f"Error al eliminar: {str(e)}"