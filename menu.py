import streamlit as st

def cerrar_sesion():
    """Cierra la sesión del usuario y reinicia el estado de sesión."""
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['page'] = 'login'  # Redirigir a la página de login

    # Eliminar posibles estados relacionados con la sesión
    for key in ['selected_option', 'login_username', 'login_password']:
        st.session_state.pop(key, None)

    st.rerun()

def home_page():
    """Página de inicio con cuatro botones."""
    if not st.session_state.get('logged_in', False):
        st.warning("Por favor, inicie sesión para continuar.")
        return  # No permite acceso si no está logueado

    # Estilo de la página
    st.markdown(
        """
        <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp {
            text-align: center;
        }
        .stButton>button {
            width: 300px;
            height: 50px;
            font-size: 20px;
            color: white;
            background-color: #062f6e;
            border-radius: 10px;
            margin: 10px;
        }
        .stButton>button:hover {
            background-color: #6acfff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Contenido del Home
    st.title("Bienvenido")
    st.subheader(f"👋 Hola, {st.session_state.get('username', 'Usuario')} 👋")
    st.subheader(f"🧠 Elige un juego 🧠")

    # Botones de navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Emociones"):
            st.session_state['page'] = 'emociones'  # Cambia la página a 'emociones'
            st.rerun()
            
    with col2:
        if st.button("Cálculo"):
            st.session_state['page'] = 'calculo'  # Cambia la página a 'calculo'
            st.rerun()

    col3, col4 = st.columns(2)
    with col3:
        if st.button("Reflejos"):
            st.session_state['page'] = 'reflejos'  # Cambia la página a 'reflejos'
            st.rerun()
    with col4:
        if st.button("🚪 Cerrar Sesión"):
            cerrar_sesion()