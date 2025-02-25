import streamlit as st
import numpy as np
import login
import menu
import formulario 
import emociones

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
        elif st.session_state['page'] == 'calculo':
            st.write("Página de Cálculo (en construcción)")  
            if st.button("Volver"):
                st.session_state['page'] = 'login'  
        elif st.session_state['page'] == 'reflejos':
            st.write("Página de Reflejos (en construcción)")  
            if st.button("Volver"):
                st.session_state['page'] = 'login'  
        elif st.session_state['page'] == 'reaccion':
            st.write("Página de reaccion (en construcción)")  
            if st.button("Volver"):
                st.session_state['page'] = 'login'  

                
    else:
        if st.session_state['page'] == 'login':
            login.login_page()
        elif st.session_state['page'] == 'registro':
            formulario.registration_page()

if __name__ == '__main__':
    main()