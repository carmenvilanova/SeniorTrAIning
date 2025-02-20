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
    st.title("Registro de Usuario")
    
    username = st.text_input("Nombre de usuario")
    password = st.text_input("Contraseña", type="password")
    
    # Botones de navegación
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Registrarse"):
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
