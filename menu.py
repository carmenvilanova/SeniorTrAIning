import streamlit as st

def cerrar_sesion():
    """Cierra la sesión del usuario y reinicia el estado de sesión."""
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['page'] = 'login'
    for key in ['selected_option', 'login_username', 'login_password']:
        st.session_state.pop(key, None)
    st.rerun()

def home_page():
    """Página de inicio optimizada para una pantalla de 6.5 x 4 cm."""
    if not st.session_state.get('logged_in', False):
        st.warning("Por favor, inicie sesión para continuar.")
        return

    st.markdown(
        """
        <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp {text-align: center;}
        .stButton>button {
            width: 100%;
            height: 80px;
            font-size: 30px;
            border-radius: 10px;
            margin: 3px 0;
        }
        .stTitle {font-size: 40px; font-weight: bold;}
        .stHeader {font-size: 36px; font-weight: bold;}
        .stSubheader {font-size: 32px;}

        p {
        font-size: 30px;
        text-align: center;
        margin: 5px 0;
        }
   
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<p class='stTitle'>Bienvenido</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='stSubheader'>👋 Hola, {st.session_state.get('username', 'Usuario')} 👋</p>", unsafe_allow_html=True)
    st.markdown("<p class='stSubheader'>🧠 Elige un juego 🧠</p>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p class='stHeader'>🎯 Juegos de Clasificación</p>", unsafe_allow_html=True)
    st.write("Prueba tu estado cognitivo con estos desafiantes juegos de clasificación!")
    if st.button("Clasificar Emociones"):
        st.session_state['page'] = 'emociones'
        st.rerun()
    if st.button("Adivina el Año"):
        st.session_state['page'] = 'adivinar_ano'
        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p class='stHeader'>🤖 Juegos con IA Generativa</p>", unsafe_allow_html=True)
    st.write("Revive el pasado con inteligencia artificial y descubre sorpresas del ayer!")
    if st.button("Juego con IA"):
        st.session_state['page'] = 'ia_juego'
        st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("🚪 Cerrar Sesión"):
        cerrar_sesion()
