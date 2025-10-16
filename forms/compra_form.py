import streamlit as st
from datetime import date
from db.db_unidades import obtener_unidades
from db.db_producto_unidad import obtener_relaciones_producto_unidad
from db.db_producto_marca import obtener_relaciones_producto_marca
from domain.compra import get_marcas_para_producto, get_unidad_para_producto

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
        st.session_state.lineas_compra.append({
            "producto": None,
            "marca": None,
            "precio": 0.0,
            "cantidad": 1,
            "unidad": None
        })
        st.rerun()

    return supermercado, fecha, st.session_state.lineas_compra

def inicializar_estado():
    if "lineas_compra" not in st.session_state:
        st.session_state.lineas_compra = []

def mostrar_linea_compra(i, productos, marcas, unidades, relaciones):
    cols = st.columns([3, 3, 2, 2, 2, 1])
    linea = st.session_state.lineas_compra[i]

    # Producto: puede estar vacío inicialmente
    if linea["producto"] is None:
        producto = cols[0].selectbox(
            "Producto", productos, key=f"prod_{i}",
            format_func=lambda x: x.nombre_producto,
            index=None
        )
    else:
        # Encontrar el índice comparando por id_producto
        producto_index = next((i for i, p in enumerate(productos) if p.id_producto == linea["producto"].id_producto), None)
        producto = cols[0].selectbox(
            "Producto", productos, key=f"prod_{i}",
            format_func=lambda x: x.nombre_producto,
            index=producto_index
        )

    # Marcas asociadas al producto seleccionado
    marcas_disponibles = []
    if producto is not None:
        relaciones_pm = obtener_relaciones_producto_marca()
        marcas_disponibles = get_marcas_para_producto(producto.id_producto, relaciones_pm, marcas)
    
    if linea["marca"] is None:
        marca = cols[1].selectbox(
            "Marca", marcas_disponibles, key=f"marca_{i}",
            format_func=lambda x: x.nombre_marca,
            index=None
        )
    else:
        # Encontrar el índice comparando por id_marca
        marca_index = next((i for i, m in enumerate(marcas_disponibles) if m.id_marca == linea["marca"].id_marca), None)
        marca = cols[1].selectbox(
            "Marca", marcas_disponibles, key=f"marca_{i}",
            format_func=lambda x: x.nombre_marca,
            index=marca_index
        )
    precio = cols[2].number_input("Precio", min_value=0.0, step=0.01, key=f"precio_{i}", value=linea["precio"])
    cantidad = cols[3].number_input("Cantidad", min_value=1, step=1, key=f"cantidad_{i}", value=linea["cantidad"])

    # --- Dropdown de unidad ---
    unidad_sel = None
    if producto is not None:
        unidad_sel = get_unidad_para_producto(producto.id_producto, relaciones, unidades)
    
    if unidad_sel:
        unidad = cols[4].selectbox(
            "Unidad", [unidad_sel], key=f"unidad_{i}",
            format_func=lambda x: x.nombre_unidad,
            index=0
        )
    else:
        unidad = None

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
