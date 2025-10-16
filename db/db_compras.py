from db.connection import session_scope
from db.models import Compra

def registrar_compras(fecha, supermercado_id, lineas):
    with session_scope() as session:
        for linea in lineas:
            compra = Compra(
                fecha=fecha,
                id_supermercado=supermercado_id,
                id_producto=linea["producto"].id_producto,
                id_marca=linea["marca"].id_marca,
                precio=linea["precio"],
                cantidad=linea["cantidad"]
            )
            session.add(compra)