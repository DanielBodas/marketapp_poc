import streamlit as st
from datetime import date

def inicializar_estado():
    if "lineas_compra" not in st.session_state:
        st.session_state.lineas_compra = []

def mostrar_linea_compra(i, productos, marcas):
    cols = st.columns([3, 3, 2, 2, 1])
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
    eliminar = cols[4].button("🗑️", key=f"del_{i}")

    # Actualizar línea
    st.session_state.lineas_compra[i] = {
        "producto": producto,
        "marca": marca,
        "precio": precio,
        "cantidad": cantidad
    }

    # Eliminar línea si se pulsa el botón
    if eliminar:
        st.session_state.lineas_compra.pop(i)
        st.rerun()

def compra_form_ui(productos, marcas, supermercados):
    st.header("🛒 Registro de Compra")

    if not productos or not marcas or not supermercados:
        st.error("❌ No se puede cargar el formulario. Verifica que existan productos, marcas y supermercados en la base de datos.")
        return None, None, []

    inicializar_estado()

    # Datos generales
    col1, col2 = st.columns(2)
    supermercado = col1.selectbox("Supermercado", supermercados, format_func=lambda x: x.nombre_supermercado)
    fecha = col2.date_input("Fecha de compra", value=date.today())

    st.subheader("🧾 Productos del ticket")

    # Mostrar líneas existentes
    for i in range(len(st.session_state.lineas_compra)):
        mostrar_linea_compra(i, productos, marcas)

    # Añadir nueva línea
    if st.button("➕ Añadir producto"):
        st.session_state.lineas_compra.append({
            "producto": productos[0],
            "marca": marcas[0],
            "precio": 0.0,
            "cantidad": 1
        })
        st.rerun()

    return supermercado, fecha, st.session_state.lineas_compra