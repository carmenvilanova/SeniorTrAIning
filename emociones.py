import streamlit as st
import random
import time
import joblib
import pandas as pd
import sqlite3
from datetime import datetime

# 🔹 Función para calcular la edad
def calcular_edad(fecha_nacimiento):
    """Calcula la edad a partir de la fecha de nacimiento."""
    hoy = datetime.today()
    edad = hoy.year - fecha_nacimiento.year
    if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
        edad -= 1
    return edad

# 🔹 Función para obtener datos del usuario desde la base de datos
def get_user_data(username):
    """Obtiene los datos del usuario desde la base de datos."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data

# 🔹 Cargar datos del juego
def load_game_data():
    return {
        "Feliz": "https://www.lavanguardia.com/files/image_449_220/uploads/2016/03/29/5fa2bd2401a8c.jpeg",
        "Triste": "https://img.freepik.com/fotos-premium/retrato-mujer-expresion-triste_641386-636.jpg",
        "Enojado": "https://image.jimcdn.com/app/cms/image/transf/dimension=410x1024:format=jpg/path/s667233d5fec7d9ab/image/idb79a0f9233d354a/version/1527621370/image.jpg",
        "Sorprendido": "https://media.istockphoto.com/id/1392578709/es/foto/tipo-afroamericano-conmocionado-mirando-hacia-otro-lado-con-expresi%C3%B3n-de-asombro.jpg?s=612x612&w=0&k=20&c=3sBViaSFcdU32rNQO4tt23L8fDrtExmt9r255DHnbdU="
    }

# 🔹 Guardar respuestas con tiempo de reacción
def save_response(user_choice, correct_answer, reaction_time):
    if "responses" not in st.session_state:
        st.session_state.responses = []
    
    st.session_state.responses.append({
        "Elección del usuario": user_choice,
        "Respuesta correcta": correct_answer,
        "Resultado": "Correcto" if user_choice == correct_answer else "Incorrecto",
        "Tiempo de reacción": reaction_time
    })
    
    if user_choice == correct_answer:
        st.session_state.correct_answers += 1  # Sumar acierto

# 🔹 Cargar nueva pregunta
def load_new_question():
    st.session_state.correct_answer, st.session_state.img_url = random.choice(list(st.session_state.game_data.items()))
    st.session_state.selected_option = None
    st.session_state.start_time_question = time.time()  # Guardar tiempo de inicio para esta pregunta

# Función decorada para cargar el modelo de Machine Learning
@st.cache_data
def cargar_modelo_y_vectorizador():
    modelo = joblib.load('models/modelo.pkl')  # Carga el modelo
    return modelo

# 🔹 Iniciar juego
def init_game():
    if "game_data" not in st.session_state:
        st.session_state.game_data = load_game_data()
        st.session_state.current_attempt = 0
        st.session_state.correct_answers = 0
        st.session_state.start_time = time.time()
        st.session_state.start_time_question = time.time()
        load_new_question()

    # Cargar el modelo de Machine Learning desde la caché
    if "ml_model" not in st.session_state:
        st.session_state.ml_model = cargar_modelo_y_vectorizador()

# 🔹 Cargar juego
def load_emotions():
    init_game()

    # Obtener los datos del usuario desde la base de datos
    username = st.session_state.get('username')  # Asegúrate de que el nombre de usuario esté en st.session_state
    user_data = get_user_data(username)

    if user_data:
        # Calcular la edad a partir de la fecha de nacimiento
        fecha_nacimiento = datetime.strptime(user_data[6], "%Y-%m-%d")  # Índice 6 es birth_date
        edad = calcular_edad(fecha_nacimiento)

        # Extraer los datos del usuario
        education_level = user_data[7]  # nivel_educativo
        gender = user_data[8]  # genero
        languages_spoken = user_data[9]  # cantidad_idiomas

        # Convertir los datos a variables dummy para el modelo
        education_level_Primary_School = 1 if education_level == "Primaria" else 0
        education_level_University = 1 if education_level == "Universidad" else 0

        gender_Male = 1 if gender == "Masculino" else 0
        gender_Other = 1 if gender == "Otro" else 0

        languages_spoken_2 = 1 if languages_spoken == "2" else 0
        languages_spoken_3 = 1 if languages_spoken == "3 o más" else 0

    # Mostrar el título del juego pequeño a la izquierda y el logo con el nombre de la app a la derecha
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 20px; padding: 10px; background-color: white; border-radius: 8px;">
            <div style="flex: 2; text-align: left; padding-right: 10px;">
                <span style="font-weight: bold;">Senior TrAIning</span>
            </div>
            <div style="flex: 2; text-align: right; padding-right: 10px;">
                <span style="font-weight: bold;">Juego de Identificación de Emociones</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Mostrar el número de intentos a la derecha y el tiempo de juego a la izquierda
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 16px; padding: 10px; background-color: white; border-radius: 8px; border: 2px solid #FFFFFF;">
        <div style="flex: 1; text-align: left; padding-left: 10px;">
            <span>⏳ Tiempo de juego: {} segundos</span>
        </div>
        <div style="flex: 1; text-align: right; padding-right: 10px;">
            <span>Ronda {}/5</span>
        </div>
    </div>
    """.format(round(time.time() - st.session_state.start_time, 2), st.session_state.current_attempt), unsafe_allow_html=True)

    # Fin del juego
    # Fin del juego
    if st.session_state.current_attempt == 5:
        total_time = round(time.time() - st.session_state.start_time, 2)
        corrects = st.session_state.correct_answers
        accuracy = corrects / 5
        average_time = sum([resp["Tiempo de reacción"] for resp in st.session_state.responses]) / 5

    #
        # Crear el DataFrame con los datos del usuario
        df = pd.DataFrame([[edad, average_time, accuracy, education_level_Primary_School, education_level_University, gender_Male, gender_Other,  languages_spoken_2, languages_spoken_3]], 
                        columns=['age', 'average_time', 'accuracy', 'education_level_Primary School', 'education_level_University',
                             'gender_Male', 'gender_Other', 'languages_spoken_2', 'languages_spoken_3'])

        # Renombrar la columna para que coincida con el nombre esperado por el modelo
        df.rename(columns={'languages_spoken_3': 'languages_spoken_3+'}, inplace=True)

        # Predecir con el modelo
        nivel_cognitivo = st.session_state.ml_model.predict(df)[0]
        probabilidades = st.session_state.ml_model.predict_proba(df)[0]

        # Redondear las probabilidades a 3 dígitos
        probabilidades_redondeadas = [round(prob, 3) for prob in probabilidades]

        # Crear una tabla de probabilidades
        prob_df = pd.DataFrame({
            'Clase': st.session_state.ml_model.classes_,
            'Probabilidad': probabilidades_redondeadas
        })

                # Mapeo de los niveles cognitivos
        nivel_cognitivo_str = ""
        if nivel_cognitivo == 0:
            nivel_cognitivo_str = "Alto"
        elif nivel_cognitivo == 1:
            nivel_cognitivo_str = "Medio"
        elif nivel_cognitivo == 2:
            nivel_cognitivo_str = "Bajo"

        # Mapeo de los valores 0, 1, 2 a Bajo, Medio, Alto
        prob_df['Clase'] = prob_df['Clase'].map({0: 'Alto', 1: 'Medio', 2: 'Bajo'})

        # Mostrar resultados con el nivel cognitivo traducido
        st.markdown("""
            <div style="text-align: center; padding: 20px; background-color: white; border-radius: 10px; border: 2px solid #FFFFFF;">
                <h3>🎉 ¡Juego Completado!</h3>
                <p>✅ Aciertos: {}</p>
                <p>⏳ Tiempo total: {} segundos</p>
                <p>🧠 Nivel Cognitivo Estimado: {}</p>
                <p>🔢 Probabilidades de la Puntuación Recibida:</p>
            </div>
            """.format(corrects, total_time, nivel_cognitivo_str), unsafe_allow_html=True)

        # Mostrar tabla de probabilidades centrada
        st.markdown("""
            <div style="display: flex; justify-content: center; align-items: center; padding: 20px;">
                <div style="text-align: center; background-color: white; border-radius: 10px; border: 2px solid #FFFFFF; padding: 20px; width: 100%; max-width: 800px;">
                    <h4>Probabilidades de la Puntuación Recibida</h4>
                    <div style="margin-left: auto; margin-right: auto;">
                        {}
                    </div>
                </div>
            </div>
        """.format(prob_df.to_html(index=False, escape=False)), unsafe_allow_html=True)


        # Botón "Jugar de nuevo"
        if st.button('🔄 Jugar de nuevo'):
            # Reiniciar el estado del juego
            st.session_state.clear()  # Limpiar todo el estado
            init_game()  # Iniciar de nuevo

        # Botón "Volver al menú"
        if st.button('🏠 Volver al menú'):
            # Reiniciar el juego
            st.session_state['page'] = 'login'  # Regresar al menú
            st.rerun()
    else:
        # Mostrar la imagen y las opciones de respuesta
        st.markdown("""
        <div style="text-align: center; padding: 30px; background-color: white; border-radius: 10px; border: 2px solid #FFFFFF;">
            <img src="{}" alt="Emoción" width="600"/>
            <h4>¿Qué emoción te sugiere la imagen?</h4>
        </div>
        """.format(st.session_state.img_url), unsafe_allow_html=True)

        # Crear los botones dentro de la cuadrícula 2x2 con tamaño fijo
        button_style = """
            <style>
                .stButton>button {
                    width: 100%; 
                    height: 100%; 
                    font-size: 18px; 
                    padding: 15px;
                    background-color: #f7f7f7;  /* Fondo gris muy claro */
                    color: black;               /* Texto negro */
                    border: 2px solid #cccccc;  /* Borde gris claro */
                    border-radius: 8px;         /* Bordes redondeados */
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);  /* Sombra suave */
                    cursor: pointer;
                    transition: all 0.3s ease;  /* Transición suave al hacer hover */
                }

                .stButton>button:hover {
                    background-color: #f7f7f7;  /* Fondo gris ligeramente más oscuro al pasar el ratón */
                    border-color: #999999;       /* Borde gris más oscuro al hacer hover */
                    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);  /* Sombra más pronunciada en hover */
                    transform: translateY(-2px);  /* Efecto de "elevación" al pasar el ratón */
                }

                .stButton>button:active {
                    background-color: #c0c0c0;  /* Fondo gris aún más oscuro cuando se hace clic */
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);  /* Sombra más suave al hacer clic */
                    transform: translateY(1px);  /* Efecto de pulsación */
                }
            </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)

        # Crear botones para las respuestas
        for i, option in enumerate(st.session_state.game_data.keys()):
            if st.button(option, key=option):
                st.session_state.selected_option = option
                reaction_time = round(time.time() - st.session_state.start_time_question, 2)
                save_response(option, st.session_state.correct_answer, reaction_time)

                if option == st.session_state.correct_answer:
                    st.success(f"¡Correcto! 🏆 (Tiempo de respuesta: {reaction_time} segundos)")
                else:
                    st.error(f"❌ Incorrecto. La respuesta correcta era: {st.session_state.correct_answer} (Tiempo de respuesta: {reaction_time} segundos)")

                # Incrementar intentos solo si no hemos alcanzado la ronda máxima (5 rondas)
                if st.session_state.current_attempt < 5:
                        st.session_state.current_attempt += 1

                time.sleep(1)
                load_new_question()
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# 🔹 Cargar la interfaz del juego
load_emotions()