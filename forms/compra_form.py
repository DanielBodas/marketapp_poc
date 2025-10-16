import streamlit as st
from datetime import date
from db.db_unidades import obtener_unidades
from db.db_producto_unidad import obtener_relaciones_producto_unidad

def compra_form_ui(productos, marcas, supermercados):
    st.header("🛒 Registro de Compra")

    if not productos or not marcas or not supermercados:
        st.error("❌ No se puede cargar el formulario. Verifica que existan productos, marcas y supermercados en la base de datos.")
        return None, None, []


    # Cargar unidades y relaciones producto-unidad
    unidades = obtener_unidades()
    relaciones = obtener_relaciones_producto_unidad()

    inicializar_estado()

    # Datos generales
    col1, col2 = st.columns(2)
    supermercado = col1.selectbox("Supermercado", supermercados, format_func=lambda x: x.nombre_supermercado)
    fecha = col2.date_input("Fecha de compra", value=date.today())

    st.subheader("🧾 Productos del ticket")


    # Mostrar líneas existentes
    for i in range(len(st.session_state.lineas_compra)):
        mostrar_linea_compra(i, productos, marcas, unidades, relaciones)


    # Añadir nueva línea
    if st.button("➕ Añadir producto"):
        # Por defecto, unidad será la primera relacionada al producto, o 'unidad' si no hay relación
        producto_default = productos[0]
        unidades_relacionadas = [u for rel in relaciones if rel.id_producto == producto_default.id_producto for u in unidades if u.id_unidad == rel.id_unidad]
        if unidades_relacionadas:
            unidad_default = unidades_relacionadas[0]
        else:
            unidad_default = next((u for u in unidades if u.nombre_unidad.lower() == "unidad"), None)
        st.session_state.lineas_compra.append({
            "producto": producto_default,
            "marca": marcas[0],
            "precio": 0.0,
            "cantidad": 1,
            "unidad": unidad_default
        })
        st.rerun()

    return supermercado, fecha, st.session_state.lineas_compra

def inicializar_estado():
    if "lineas_compra" not in st.session_state:
        st.session_state.lineas_compra = []

def mostrar_linea_compra(i, productos, marcas, unidades, relaciones):
    cols = st.columns([3, 3, 2, 2, 2, 1])
    linea = st.session_state.lineas_compra[i]

    producto = cols[0].selectbox(
        "Producto", productos, key=f"prod_{i}",
        format_func=lambda x: x.nombre_producto,
        index=productos.index(linea["producto"]) if linea["producto"] in productos else 0
    )
    marca = cols[1].selectbox(
        "Marca", marcas, key=f"marca_{i}",
        format_func=lambda x: x.nombre_marca,
        index=marcas.index(linea["marca"]) if linea["marca"] in marcas else 0
    )
    precio = cols[2].number_input("Precio", min_value=0.0, step=0.01, key=f"precio_{i}", value=linea["precio"])
    cantidad = cols[3].number_input("Cantidad", min_value=1, step=1, key=f"cantidad_{i}", value=linea["cantidad"])

    # --- Dropdown de unidad ---
    unidades_relacionadas = [u for rel in relaciones if rel.id_producto == producto.id_producto for u in unidades if u.id_unidad == rel.id_unidad]
    if unidades_relacionadas:
        unidad_default = unidades_relacionadas[0]
        unidad = cols[4].selectbox(
            "Unidad", unidades_relacionadas, key=f"unidad_{i}",
            format_func=lambda x: x.nombre_unidad,
            index=unidades_relacionadas.index(linea["unidad"]) if linea["unidad"] in unidades_relacionadas else 0
        )
    else:
        unidad_unica = next((u for u in unidades if u.nombre_unidad.lower() == "unidad"), None)
        unidad = cols[4].selectbox(
            "Unidad", [unidad_unica] if unidad_unica else [], key=f"unidad_{i}",
            format_func=lambda x: x.nombre_unidad,
            index=0
        )

    eliminar = cols[5].button("🗑️", key=f"del_{i}")

    # Actualizar línea
    st.session_state.lineas_compra[i] = {
        "producto": producto,
        "marca": marca,
        "precio": precio,
        "cantidad": cantidad,
        "unidad": unidad
    }

    # Eliminar línea si se pulsa el botón
    if eliminar:
        st.session_state.lineas_compra.pop(i)
        st.rerun()
