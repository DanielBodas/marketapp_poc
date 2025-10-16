import streamlit as st

from forms.landing_page import landing_page

st.set_page_config(page_title="Gestor de Compras", page_icon="🛒", layout="wide")

def main():
    landing_page()

if __name__ == "__main__":
    main()