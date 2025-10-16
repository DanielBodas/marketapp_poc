from db.connection import get_session
from db.models import Marca
from sqlalchemy.exc import IntegrityError

def obtener_marcas():
    session = get_session()
    return session.query(Marca).order_by(Marca.nombre_marca).all()

def insertar_marca(nombre: str):
    session = get_session()
    nueva = Marca(nombre_marca=nombre)
    session.add(nueva)
    try:
        session.commit()
        return True, "Marca registrada correctamente."
    except IntegrityError:
        session.rollback()
        return False, "Ya existe una marca con ese nombre."
    except Exception as e:
        session.rollback()
        return False, f"Error inesperado: {str(e)}"

def actualizar_marca(id_marca: int, nuevo_nombre: str):
    session = get_session()
    marca = session.get(Marca, id_marca)
    if marca:
        marca.nombre_marca = nuevo_nombre
        try:
            session.commit()
            return True, "Marca actualizada correctamente."
        except IntegrityError:
            session.rollback()
            return False, "Ya existe otra marca con ese nombre."
        except Exception as e:
            session.rollback()
            return False, f"Error inesperado: {str(e)}"
    return False, "Marca no encontrada."

def eliminar_marca(id_marca: int):
    session = get_session()
    marca = session.get(Marca, id_marca)
    if marca:
        try:
            session.delete(marca)
            session.commit()
            return True, "Marca eliminada correctamente."
        except Exception as e:
            session.rollback()
            return False, f"Error al eliminar: {str(e)}"
    return False, "Marca no encontrada."