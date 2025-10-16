import streamlit as st
from forms.producto_marca_form import producto_marca_crud_ui

st.set_page_config(page_title="Productos y Marcas", page_icon="📦", layout="wide")

def main():
    producto_marca_crud_ui()

if __name__ == "__main__":
    main()