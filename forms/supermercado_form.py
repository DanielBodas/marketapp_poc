import streamlit as st
from db.db_supermercados import (
    obtener_supermercados,
    insertar_supermercado,
    actualizar_supermercado,
    eliminar_supermercado
)
from utils.db_errors import mostrar_error_db

def supermercado_crud_ui():
    st.header("🏬 Gestión de Supermercados")

    try:
        supermercados = obtener_supermercados()
    except Exception as e:
        mostrar_error_db(e, contexto="Carga de supermercados")
        return

    # --- Crear nuevo supermercado ---
    with st.container():
        st.subheader("➕ Añadir nuevo supermercado")
        with st.form("form_nuevo_supermercado", clear_on_submit=True):
            nuevo_nombre = st.text_input("📝 Nombre del supermercado", placeholder="Ej. Mercadona, Carrefour...")
            submitted = st.form_submit_button("💾 Guardar")

            if submitted:
                if not nuevo_nombre.strip():
                    st.warning("⚠️ El nombre no puede estar vacío.")
                else:
                    try:
                        ok, mensaje = insertar_supermercado(nuevo_nombre.strip())
                        if ok:
                            st.success(mensaje)
                            st.rerun()
                        else:
                            st.error(mensaje)
                    except Exception as e:
                        mostrar_error_db(e, contexto="Registro de supermercado")

    st.markdown("---")

    # --- Listar y editar existentes ---
    st.subheader("📋 Supermercados registrados")
    for supermercado in supermercados:
        with st.expander(f"🛒 {supermercado.nombre_supermercado}"):
            with st.form(f"form_edit_{supermercado.id_supermercado}"):
                nuevo_nombre = st.text_input("✏️ Editar nombre", value=supermercado.nombre_supermercado)
                col1, col2 = st.columns([6, 6])
                actualizar = col1.form_submit_button("✅ Actualizar")
                eliminar = col2.form_submit_button("🗑️ Eliminar")

                if actualizar:
                    if not nuevo_nombre.strip():
                        st.warning("⚠️ El nombre no puede estar vacío.")
                    else:
                        try:
                            ok, mensaje = actualizar_supermercado(supermercado.id_supermercado, nuevo_nombre.strip())
                            if ok:
                                st.success(mensaje)
                                st.rerun()
                            else:
                                st.error(mensaje)
                        except Exception as e:
                            mostrar_error_db(e, contexto="Actualización de supermercado")

                if eliminar:
                    try:
                        ok, mensaje = eliminar_supermercado(supermercado.id_supermercado)
                        if ok:
                            st.success(mensaje)
                            st.rerun()
                        else:
                            st.error(mensaje)
                    except Exception as e:
                        mostrar_error_db(e, contexto="Eliminación de supermercado")