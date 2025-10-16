import streamlit as st
from db.db_productos import obtener_productos
from db.db_marcas import obtener_marcas
from db.db_supermercados import obtener_supermercados
from db.db_compras import registrar_compras
from forms.compra_form import compra_form_ui
from utils.db_errors import mostrar_error_db

st.set_page_config(page_title="Registro de Compras", page_icon="🛒", layout="wide")

def main():
    try:
        productos = obtener_productos()
        marcas = obtener_marcas()
        supermercados = obtener_supermercados()

        supermercado, fecha, lineas = compra_form_ui(productos, marcas, supermercados)

        if st.button("💾 Guardar compra"):
            if not lineas:
                st.warning("Debes añadir al menos un producto.")
            else:
                registrar_compras(fecha, supermercado.id_supermercado, lineas)
                st.success("✅ Compra registrada correctamente.")
                st.session_state.lineas_compra = []

    except Exception as e:
        mostrar_error_db(e, context="Registro de compra")

if __name__ == "__main__":
    main()