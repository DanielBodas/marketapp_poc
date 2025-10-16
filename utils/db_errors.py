import streamlit as st
import sqlalchemy.exc

def handle_db_error(error: Exception, context: str = "Error en la base de datos"):
    if isinstance(error, sqlalchemy.exc.OperationalError):
        st.error(f"❌ {context}: error de conexión con Supabase.")
    elif isinstance(error, sqlalchemy.exc.ProgrammingError):
        st.error(f"❌ {context}: error de sintaxis o permisos.")
    elif isinstance(error, sqlalchemy.exc.IntegrityError):
        st.error(f"❌ {context}: violación de integridad (duplicado, clave foránea, etc.).")
    else:
        st.error(f"❌ {context}: error inesperado.")
    st.exception(error)

import streamlit as st
import sqlalchemy.exc

def mostrar_error_db(error: Exception, contexto: str = "Error en la base de datos"):
    if isinstance(error, sqlalchemy.exc.OperationalError):
        st.error(f"❌ {contexto}: error de conexión con Supabase.")
    elif isinstance(error, sqlalchemy.exc.ProgrammingError):
        st.error(f"❌ {contexto}: error de sintaxis o permisos.")
    elif isinstance(error, sqlalchemy.exc.IntegrityError):
        st.error(f"❌ {contexto}: violación de integridad (duplicado, clave foránea, etc.).")
    else:
        st.error(f"❌ {contexto}: error inesperado.")
    st.exception(error)