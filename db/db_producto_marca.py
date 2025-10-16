from db.connection import get_session
from db.models import ProductoMarca
from sqlalchemy.exc import IntegrityError

def obtener_relaciones_producto_marca():
    session = get_session()
    return session.query(ProductoMarca).all()

def insertar_relacion_producto_marca(id_producto: int, id_marca: int):
    session = get_session()
    nueva = ProductoMarca(id_producto=id_producto, id_marca=id_marca)
    session.add(nueva)
    try:
        session.commit()
        return True, "Relación producto-marca creada."
    except IntegrityError:
        session.rollback()
        return False, "La relación ya existe."
    except Exception as e:
        session.rollback()
        return False, f"Error inesperado: {str(e)}"

def eliminar_relacion_producto_marca(id_producto_marca: int):
    session = get_session()
    relacion = session.get(ProductoMarca, id_producto_marca)
    if relacion:
        try:
            session.delete(relacion)
            session.commit()
            return True, "Relación eliminada."
        except Exception as e:
            session.rollback()
            return False, f"Error al eliminar: {str(e)}"
    return False, "Relación no encontrada."