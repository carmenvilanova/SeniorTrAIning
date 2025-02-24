import streamlit as st
import sqlite3

def check_user_exists(username):
    """Verifica si el nombre de usuario ya existe en la base de datos."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def add_user(username, password):
    """Agrega un nuevo usuario a la base de datos."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def registration_page():
    st.markdown("""
    <style>
        .title-container {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            padding: 20px;
            background-color: white;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .title-container img {
            width: 40px;
            margin-right: 15px;
        }
        .title-container h1 {
            font-weight: bold;
        }
        .form-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        }
        .form-container input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
        .button-container {
            display: flex;
            justify-content: space-between;
            width: 100%;
        }
        .button-container button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .button-container button:hover {
            background-color: #45a049;
        }
    </style>
    """, unsafe_allow_html=True)

    # Contenedor con el logo a la izquierda y el título al centro
    st.markdown("""
    <div class="title-container">
        <img src="https://your-logo-url.com/logo.png" alt="Logo">
        <h1>Registro de Usuario</h1>
    </div>
    """, unsafe_allow_html=True)

    # Formulario de registro
    with st.form(key='registration_form'):
        username = st.text_input("Nombre de usuario")
        password = st.text_input("Contraseña", type="password")
        submit_button = st.form_submit_button("Registrarse")
        
        # Botones de navegación
        col1, col2 = st.columns(2)
        with col1:
            if submit_button:
                if username and password:
                    if check_user_exists(username):
                        st.error("El nombre de usuario ya existe. Inténtalo con otro.")
                    else:
                        try:
                            add_user(username, password)
                            st.success("Usuario registrado con éxito. Ahora puedes iniciar sesión.")
                            st.session_state['page'] = 'login'
                            st.rerun()
                        except sqlite3.Error as e:
                            st.error(f"Error al registrar el usuario: {e}")
                else:
                    st.error("Por favor, completa todos los campos.")
        with col2:
            if st.button("Volver"):
                st.session_state['page'] = 'login'  
                st.rerun()
