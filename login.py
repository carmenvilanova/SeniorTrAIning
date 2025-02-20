import streamlit as st
import sqlite3

def check_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_background_color():
    background_color_html = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    h1, h3 {
        font-family: "Raleway", Sans-serif;
        color: #062f6e;
    }
    div[data-testid="stTextInput"] label {
        color: white;
    }
    
    .stButton>button {
        display: block;
        margin: 0 auto;
    }

    </style>
    """
    st.markdown(background_color_html, unsafe_allow_html=True)

def login_page():
    add_background_color()
    
    with st.container():
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        
        st.markdown("<h1 style='text-align: center; font-size: 62px;'>SENIOR TRAINING</h1>", unsafe_allow_html=True)

        username = st.text_input("USUARIO", key='login_username')
        password = st.text_input("CONTRASEÑA", type="password", key='login_password')

        if st.button("INICIAR SESIÓN"):
            if check_user(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

        # 🔹 Botón para ir a la página de registro
        if st.button("¿No tienes una cuenta? Regístrate aquí"):
            st.session_state['page'] = 'registro'
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        st.image("img/logo.jpg", width=650)
