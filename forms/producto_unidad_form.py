import streamlit as st
from db.db_productos import obtener_productos
from db.db_unidades import obtener_unidades
from db.db_producto_unidad import (
    obtener_relaciones_producto_unidad,
    insertar_relacion_producto_unidad,
    eliminar_relacion_producto_unidad,
)
from utils.db_errors import mostrar_error_db


def producto_unidad_crud_ui():
    st.header("⚖️ Asociar Productos y Unidades")

    try:
        productos = obtener_productos()
        unidades = obtener_unidades()
        relaciones = obtener_relaciones_producto_unidad()
    except Exception as e:
        mostrar_error_db(e, contexto="Carga de datos para producto-unidad")
        return

    st.subheader("🔗 Relacionar producto con unidad")
    with st.form("form_relacion_producto_unidad"):
        producto_sel = st.selectbox("Producto", productos, format_func=lambda x: x.nombre_producto)
        unidad_sel = st.selectbox("Unidad", unidades, format_func=lambda x: x.nombre_unidad)
        if st.form_submit_button("🔗 Crear relación"):
            try:
                ok, msg = insertar_relacion_producto_unidad(producto_sel.id_producto, unidad_sel.id_unidad)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            except Exception as e:
                mostrar_error_db(e, contexto="Relación producto-unidad")

    st.markdown("---")

    st.subheader("📋 Relaciones existentes")
    for rel in relaciones:
        prod = next((p for p in productos if p.id_producto == rel.id_producto), None)
        unidad = next((u for u in unidades if u.id_unidad == rel.id_unidad), None)
        if prod and unidad:
            with st.expander(f"{prod.nombre_producto} ↔ {unidad.nombre_unidad}"):
                if st.button("🗑️ Eliminar relación", key=f"del_rel_un_{rel.id_producto_unidad}"):
                    try:
                        ok, msg = eliminar_relacion_producto_unidad(rel.id_producto_unidad)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    except Exception as e:
                        mostrar_error_db(e, contexto="Eliminación de relación producto-unidad")
