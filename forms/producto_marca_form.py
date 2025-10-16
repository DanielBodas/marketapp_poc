import streamlit as st
from db.db_productos import (
    obtener_productos,
    insertar_producto,
    actualizar_producto,
    eliminar_producto,
)
from db.db_marcas import (
    obtener_marcas,
    insertar_marca,
    actualizar_marca,
    eliminar_marca,
)
from db.db_producto_marca import (
    obtener_relaciones_producto_marca,
    insertar_relacion_producto_marca,
    eliminar_relacion_producto_marca,
)
from utils.db_errors import mostrar_error_db

def producto_marca_crud_ui():
    st.header("📦 Gestión de Productos y Marcas")

    try:
        productos = obtener_productos()
        marcas = obtener_marcas()
        relaciones = obtener_relaciones_producto_marca()
    except Exception as e:
        mostrar_error_db(e, contexto="Carga de datos")
        return

    col1, col2 = st.columns(2)

    # --- Crear producto ---
    with col1:
        with st.form("form_nuevo_producto", clear_on_submit=True):
            nuevo_producto = st.text_input("🆕 Nombre del producto")
            guardar_producto = st.form_submit_button("💾 Guardar producto")

        if guardar_producto:
            if not nuevo_producto.strip():
                st.warning("⚠️ El nombre del producto no puede estar vacío.")
            else:
                try:
                    ok, msg = insertar_producto(nuevo_producto.strip())
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                except Exception as e:
                    mostrar_error_db(e, contexto="Registro de producto")

    # --- Crear marca ---
    with col2:
        with st.form("form_nueva_marca", clear_on_submit=True):
            nueva_marca = st.text_input("🆕 Nombre de la marca")
            guardar_marca = st.form_submit_button("💾 Guardar marca")

        if guardar_marca:
            if not nueva_marca.strip():
                st.warning("⚠️ El nombre de la marca no puede estar vacío.")
            else:
                try:
                    ok, msg = insertar_marca(nueva_marca.strip())
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                except Exception as e:
                    mostrar_error_db(e, contexto="Registro de marca")

    st.markdown("---")


    # --- Relación producto ↔ marca ---
    st.subheader("🔗 Relacionar producto con marca")
    with st.form("form_relacion_producto_marca"):
        producto_sel = st.selectbox("Producto", productos, format_func=lambda x: x.nombre_producto)
        marca_sel = st.selectbox("Marca", marcas, format_func=lambda x: x.nombre_marca)
        if st.form_submit_button("🔗 Crear relación"):
            try:
                ok, msg = insertar_relacion_producto_marca(producto_sel.id_producto, marca_sel.id_marca)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
            except Exception as e:
                mostrar_error_db(e, contexto="Relación producto-marca")

    st.markdown("---")

    # --- Mostrar relaciones existentes ---
    st.subheader("📋 Relaciones existentes")
    for rel in relaciones:
        prod = next((p for p in productos if p.id_producto == rel.id_producto), None)
        marca = next((m for m in marcas if m.id_marca == rel.id_marca), None)
        if prod and marca:
            with st.expander(f"{prod.nombre_producto} ↔ {marca.nombre_marca}"):
                if st.button("🗑️ Eliminar relación", key=f"del_rel_{rel.id_producto_marca}"):
                    try:
                        ok, msg = eliminar_relacion_producto_marca(rel.id_producto_marca)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
                    except Exception as e:
                        mostrar_error_db(e, contexto="Eliminación de relación")