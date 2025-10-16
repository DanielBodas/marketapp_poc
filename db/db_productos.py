from db.connection import get_session
from db.models import Producto
from sqlalchemy.exc import IntegrityError

def obtener_productos():
    session = get_session()
    return session.query(Producto).order_by(Producto.nombre_producto).all()

def insertar_producto(nombre: str):
    session = get_session()
    nuevo = Producto(nombre_producto=nombre)
    session.add(nuevo)
    try:
        session.commit()
        return True, "Producto registrado correctamente."
    except IntegrityError:
        session.rollback()
        return False, "Ya existe un producto con ese nombre."
    except Exception as e:
        session.rollback()
        return False, f"Error inesperado: {str(e)}"

def actualizar_producto(id_producto: int, nuevo_nombre: str):
    session = get_session()
    producto = session.query(Producto).get(id_producto)
    if producto:
        producto.nombre_producto = nuevo_nombre
        try:
            session.commit()
            return True, "Producto actualizado correctamente."
        except IntegrityError:
            session.rollback()
            return False, "Ya existe otro producto con ese nombre."
        except Exception as e:
            session.rollback()
            return False, f"Error inesperado: {str(e)}"
    return False, "Producto no encontrado."

def eliminar_producto(id_producto: int):
    session = get_session()
    producto = session.query(Producto).get(id_producto)
    if producto:
        try:
            session.delete(producto)
            session.commit()
            return True, "Producto eliminado correctamente."
        except Exception as e:
            session.rollback()
            return False, f"Error al eliminar: {str(e)}"
    return False, "Producto no encontrado."