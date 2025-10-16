import streamlit as st
from db.db_unidades import (
    obtener_unidades,
    insertar_unidad,
    actualizar_unidad,
    eliminar_unidad,
)
from db.db_productos import obtener_productos
from db.db_producto_unidad import (
    obtener_relaciones_producto_unidad,
    insertar_relacion_producto_unidad,
    eliminar_relacion_producto_unidad,
)
from utils.db_errors import mostrar_error_db


def unidad_crud_ui():
    st.header("⚖️ Gestión de Unidades")

    try:
        unidades = obtener_unidades()
    except Exception as e:
        mostrar_error_db(e, contexto="Carga de unidades")
        return

    # Crear nueva unidad
    with st.container():
        st.subheader("➕ Añadir nueva unidad")
        with st.form("form_nueva_unidad", clear_on_submit=True):
            nuevo_nombre = st.text_input("📝 Nombre de la unidad", placeholder="Ej. unidad, litro, kg")
            submitted = st.form_submit_button("💾 Guardar")

            if submitted:
                if not nuevo_nombre.strip():
                    st.warning("⚠️ El nombre no puede estar vacío.")
                else:
                    try:
                        ok, mensaje = insertar_unidad(nuevo_nombre.strip())
                        if ok:
                            st.success(mensaje)
                            st.rerun()
                        else:
                            st.error(mensaje)
                    except Exception as e:
                        mostrar_error_db(e, contexto="Registro de unidad")

    st.markdown("---")

    # Listar y editar unidades
    st.subheader("📋 Unidades registradas")
    for unidad in unidades:
        with st.expander(f"{unidad.nombre_unidad}"):
            with st.form(f"form_edit_unidad_{unidad.id_unidad}"):
                nuevo_nombre = st.text_input("✏️ Editar nombre", value=unidad.nombre_unidad)
                col1, col2 = st.columns([6, 6])
                actualizar = col1.form_submit_button("✅ Actualizar")
                eliminar = col2.form_submit_button("🗑️ Eliminar")

                if actualizar:
                    if not nuevo_nombre.strip():
                        st.warning("⚠️ El nombre no puede estar vacío.")
                    else:
                        try:
                            ok, mensaje = actualizar_unidad(unidad.id_unidad, nuevo_nombre.strip())
                            if ok:
                                st.success(mensaje)
                                st.rerun()
                            else:
                                st.error(mensaje)
                        except Exception as e:
                            mostrar_error_db(e, contexto="Actualización de unidad")

                if eliminar:
                    try:
                        ok, mensaje = eliminar_unidad(unidad.id_unidad)
                        if ok:
                            st.success(mensaje)
                            st.rerun()
                        else:
                            st.error(mensaje)
                    except Exception as e:
                        mostrar_error_db(e, contexto="Eliminación de unidad")

    st.markdown("---")

    # --- Relación producto ↔ unidad ---
    st.subheader("🔗 Relacionar producto con unidad")
    try:
        productos = obtener_productos()
        relaciones = obtener_relaciones_producto_unidad()
    except Exception as e:
        mostrar_error_db(e, contexto="Carga de datos para relaciones")
        return

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
