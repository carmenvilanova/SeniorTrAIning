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
    """Página de inicio con dos categorías de juegos."""
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
            border-radius: 10px;
            margin: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Contenido del Home
    st.title("Bienvenido")
    st.subheader(f"👋 Hola, {st.session_state.get('username', 'Usuario')} 👋")
    st.subheader(f"🧠 Elige un juego 🧠")
    st.write("---")

    # Organización en dos columnas
    col1, col2 = st.columns(2)

    # Juegos de Clasificación
    with col1:
        st.header("🎯 Juegos de Clasificación")
        st.write("Prueba tu estado cognitivo con estos desafiantes juegos de clasificación!")
        if st.button("Clasificar Emociones"):
            st.session_state['page'] = 'emociones'
            st.rerun()
        if st.button("Adivina el Año"):
            st.session_state['page'] = 'adivinar_ano'
            st.rerun()

    # Juegos con IA Generativa
    with col2:
        st.header("🤖 Juegos con IA Generativa")
        st.write("Revive el pasado con inteligencia artificial y descubre sorpresas del ayer!")
        if st.button("Juego con IA"):
            st.session_state['page'] = 'ia_juego'
            st.rerun()

    st.write("---")

    # Botón de cerrar sesión
    if st.button("🚪 Cerrar Sesión"):
        cerrar_sesion()
