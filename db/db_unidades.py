from db.connection import session_scope, get_session
from db.models import Unidad
from sqlalchemy.exc import IntegrityError


def obtener_unidades():
    session = get_session()
    return session.query(Unidad).order_by(Unidad.nombre_unidad).all()


def insertar_unidad(nombre: str):
    nueva = Unidad(nombre_unidad=nombre)
    try:
        with session_scope() as session:
            session.add(nueva)
        return True, "Unidad registrada correctamente."
    except IntegrityError:
        return False, "Ya existe una unidad con ese nombre."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"


def actualizar_unidad(id_unidad: int, nuevo_nombre: str):
    try:
        with session_scope() as session:
            unidad = session.get(Unidad, id_unidad)
            if not unidad:
                return False, "Unidad no encontrada."
            unidad.nombre_unidad = nuevo_nombre
        return True, "Unidad actualizada correctamente."
    except IntegrityError:
        return False, "Ya existe otra unidad con ese nombre."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"


def eliminar_unidad(id_unidad: int):
    try:
        with session_scope() as session:
            unidad = session.get(Unidad, id_unidad)
            if not unidad:
                return False, "Unidad no encontrada."
            session.delete(unidad)
        return True, "Unidad eliminada correctamente."
    except Exception as e:
        return False, f"Error al eliminar: {str(e)}"
