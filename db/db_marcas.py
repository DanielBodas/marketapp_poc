from db.connection import get_session, session_scope
from db.models import Marca
from sqlalchemy.exc import IntegrityError

def obtener_marcas():
    session = get_session()
    return session.query(Marca).order_by(Marca.nombre_marca).all()

def insertar_marca(nombre: str):
    nueva = Marca(nombre_marca=nombre)
    try:
        with session_scope() as session:
            session.add(nueva)
        return True, "Marca registrada correctamente."
    except IntegrityError:
        return False, "Ya existe una marca con ese nombre."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"

def actualizar_marca(id_marca: int, nuevo_nombre: str):
    try:
        with session_scope() as session:
            marca = session.get(Marca, id_marca)
            if not marca:
                return False, "Marca no encontrada."
            marca.nombre_marca = nuevo_nombre
        return True, "Marca actualizada correctamente."
    except IntegrityError:
        return False, "Ya existe otra marca con ese nombre."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"

def eliminar_marca(id_marca: int):
    try:
        with session_scope() as session:
            marca = session.get(Marca, id_marca)
            if not marca:
                return False, "Marca no encontrada."
            session.delete(marca)
        return True, "Marca eliminada correctamente."
    except Exception as e:
        return False, f"Error al eliminar: {str(e)}"