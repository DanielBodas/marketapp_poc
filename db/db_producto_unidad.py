from db.connection import session_scope, get_session
from db.models import ProductoUnidad
from sqlalchemy.exc import IntegrityError


def obtener_relaciones_producto_unidad():
    session = get_session()
    return session.query(ProductoUnidad).all()


def insertar_relacion_producto_unidad(id_producto: int, id_unidad: int):
    nueva = ProductoUnidad(id_producto=id_producto, id_unidad=id_unidad)
    try:
        with session_scope() as session:
            session.add(nueva)
        return True, "Relación producto-unidad creada."
    except IntegrityError:
        return False, "La relación ya existe."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"


def eliminar_relacion_producto_unidad(id_producto_unidad: int):
    try:
        with session_scope() as session:
            relacion = session.get(ProductoUnidad, id_producto_unidad)
            if not relacion:
                return False, "Relación no encontrada."
            session.delete(relacion)
        return True, "Relación eliminada."
    except Exception as e:
        return False, f"Error al eliminar: {str(e)}"
