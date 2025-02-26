import streamlit as st
import numpy as np
import login
import menu
import formulario 
import emociones
import Ia_juego

def main():
    # Inicializar el estado de sesión si no existe
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'  # Página por defecto
        
    # Controlar la navegación
    if st.session_state['logged_in']:
        if st.session_state['page'] == 'login':
            menu.home_page()
        elif st.session_state['page'] == 'emociones':
            emociones.load_emotions()
        elif st.session_state['page'] == 'adivinar_ano':
            st.write("Página de Adivinar año (en construcción)")  
            if st.button("Volver"):
                st.session_state['page'] = 'login'  
        elif st.session_state['page'] == 'ia_juego':
            Ia_juego.load_ia_game() 

                
    else:
        if st.session_state['page'] == 'login':
            login.login_page()
        elif st.session_state['page'] == 'registro':
            formulario.registration_page()

if __name__ == '__main__':
    main()