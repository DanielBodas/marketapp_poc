import streamlit as st
from config.routes import PAGES

def landing_page():

    st.markdown("<h1 style='text-align: center;'>🛍️ Bienvenido al Gestor de Compras</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Organiza tus tickets, productos y supermercados de forma eficiente</h4>", unsafe_allow_html=True)
    st.divider()

    # Ordenar por clave numérica
    ordenadas = sorted(PAGES.items(), key=lambda x: x[0])

    # Mostrar en columnas de 3
    for i in range(0, len(ordenadas), 3):
        cols = st.columns(3)
        for j, (clave, datos) in enumerate(ordenadas[i:i+3]):
            with cols[j]:
                st.image(datos["image"], width=80)
                st.subheader(datos["label"])
                st.write(datos["description"])
                st.page_link(datos["file"], label=f"Ir a {datos['label'].lower()}", icon=datos["icon"])

    st.divider()
    st.markdown("""
    <div style='text-align: center; font-size: 0.9em; color: gray;'>
        Desarrollado por Daniel • Arquitectura modular y dinámica • Streamlit + Supabase
    </div>
    """, unsafe_allow_html=True)