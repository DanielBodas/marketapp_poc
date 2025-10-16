import streamlit as st
from forms.supermercado_form import supermercado_crud_ui

st.set_page_config(page_title="Gestión de Supermercados", page_icon="🏬", layout="wide")

def main():
    supermercado_crud_ui()

if __name__ == "__main__":
    main()