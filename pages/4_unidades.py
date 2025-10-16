import streamlit as st
from forms.unidad_form import unidad_crud_ui

st.set_page_config(page_title="Unidades", page_icon="⚖️", layout="wide")


def main():
    unidad_crud_ui()


if __name__ == "__main__":
    main()
