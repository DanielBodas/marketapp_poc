from db.connection import get_session, session_scope
from db.models import Producto
from sqlalchemy.exc import IntegrityError

def obtener_productos():
    session = get_session()
    return session.query(Producto).order_by(Producto.nombre_producto).all()

def insertar_producto(nombre: str):
    nuevo = Producto(nombre_producto=nombre)
    try:
        with session_scope() as session:
            session.add(nuevo)
        return True, "Producto registrado correctamente."
    except IntegrityError:
        return False, "Ya existe un producto con ese nombre."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"

def actualizar_producto(id_producto: int, nuevo_nombre: str):
    try:
        with session_scope() as session:
            producto = session.get(Producto, id_producto)
            if not producto:
                return False, "Producto no encontrado."
            producto.nombre_producto = nuevo_nombre
        return True, "Producto actualizado correctamente."
    except IntegrityError:
        return False, "Ya existe otro producto con ese nombre."
    except Exception as e:
        return False, f"Error inesperado: {str(e)}"

def eliminar_producto(id_producto: int):
    try:
        with session_scope() as session:
            producto = session.get(Producto, id_producto)
            if not producto:
                return False, "Producto no encontrado."
            session.delete(producto)
        return True, "Producto eliminado correctamente."
    except Exception as e:
        return False, f"Error al eliminar: {str(e)}"