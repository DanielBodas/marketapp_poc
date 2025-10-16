from db.connection import get_session, session_scope
from db.models import Supermercado
from sqlalchemy.exc import IntegrityError

def obtener_supermercados():
    session = get_session()
    return session.query(Supermercado).order_by(Supermercado.nombre_supermercado).all()

def insertar_supermercado(nombre: str):
    nuevo = Supermercado(nombre_supermercado=nombre)
    try:
        with session_scope() as session:
            session.add(nuevo)
        return True, "Supermercado registrado correctamente."
    except IntegrityError:
        return False, "Ya existe un supermercado con ese nombre."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"

def actualizar_supermercado(id_supermercado: int, nuevo_nombre: str):
    try:
        with session_scope() as session:
            supermercado = session.get(Supermercado, id_supermercado)
            if not supermercado:
                return False, "Supermercado no encontrado."
            supermercado.nombre_supermercado = nuevo_nombre
        return True, "Supermercado actualizado correctamente."
    except IntegrityError:
        return False, "Ya existe otro supermercado con ese nombre."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"

def eliminar_supermercado(id_supermercado: int):
    try:
        with session_scope() as session:
            supermercado = session.get(Supermercado, id_supermercado)
            if not supermercado:
                return False, "Supermercado no encontrado."
            session.delete(supermercado)
        return True, "Supermercado eliminado correctamente."
    except Exception as e:
        return False, f"Error al eliminar: {str(e)}"