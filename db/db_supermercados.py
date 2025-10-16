from db.connection import get_session
from db.models import Supermercado
from sqlalchemy.exc import IntegrityError

def obtener_supermercados():
    session = get_session()
    return session.query(Supermercado).order_by(Supermercado.nombre_supermercado).all()

def insertar_supermercado(nombre: str):
    session = get_session()
    nuevo = Supermercado(nombre_supermercado=nombre)
    session.add(nuevo)
    try:
        session.commit()
        return True, "Supermercado registrado correctamente."
    except IntegrityError:
        session.rollback()
        return False, "Ya existe un supermercado con ese nombre."
    except Exception as e:
        session.rollback()
        return False, f"Error inesperado: {str(e)}"

def actualizar_supermercado(id_supermercado: int, nuevo_nombre: str):
    session = get_session()
    supermercado = session.get(Supermercado, id_supermercado)
    if supermercado:
        supermercado.nombre_supermercado = nuevo_nombre
        try:
            session.commit()
            return True, "Supermercado actualizado correctamente."
        except IntegrityError:
            session.rollback()
            return False, "Ya existe otro supermercado con ese nombre."
        except Exception as e:
            session.rollback()
            return False, f"Error inesperado: {str(e)}"
    return False, "Supermercado no encontrado."

def eliminar_supermercado(id_supermercado: int):
    session = get_session()
    supermercado = session.get(Supermercado, id_supermercado)
    if supermercado:
        try:
            session.delete(supermercado)
            session.commit()
            return True, "Supermercado eliminado correctamente."
        except Exception as e:
            session.rollback()
            return False, f"Error al eliminar: {str(e)}"
    return False, "Supermercado no encontrado."