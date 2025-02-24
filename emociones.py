import streamlit as st
import random
import time
import joblib
import pandas as pd

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
    modelo = joblib.load('modelo.pkl')  # Carga el modelo
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
            <span>Ronda {}/10</span>
        </div>
    </div>
    """.format(round(time.time() - st.session_state.start_time, 2), st.session_state.current_attempt), unsafe_allow_html=True)

    # Fin del juego
    if st.session_state.current_attempt > 10:
        total_time = round(time.time() - st.session_state.start_time, 2)
        corrects = st.session_state.correct_answers
        age = 60
        average_time = 0.86
        education_level_High_School = 1
        education_level_Primary_School = 0
        education_level_University = 0
        gender_Female = 0
        gender_Male = 1
        gender_Other = 0
        languages_spoken_1 = 0
        languages_spoken_2 = 1
        gender = 1
        accuracy = corrects / 10
        average_time = sum([resp["Tiempo de reacción"] for resp in st.session_state.responses]) / 10

        df = pd.DataFrame([[age, average_time, accuracy, education_level_High_School, education_level_Primary_School, education_level_University, gender_Female, gender_Male, gender_Other, languages_spoken_1, languages_spoken_2]], 
                          columns=['age', 'average_time', 'accuracy', 'education_level_High School', 'education_level_Primary School', 'education_level_University',
                                   'gender_Female', 'gender_Male', 'gender_Other', 'languages_spoken_1', 'languages_spoken_2'])
        # Predecir con el modelo
        nivel_cognitivo = st.session_state.ml_model.predict(df)[0]

        # Mostrar resultados en un div con recuadro gris
        st.markdown("""
        <div style="text-align: center; padding: 20px; background-color: white; border-radius: 10px; border: 2px solid #FFFFFF;">
            <h3>🎉 ¡Juego Completado!</h3>
            <p>✅ Aciertos: {}</p>
            <p>⏳ Tiempo total: {} segundos</p>
            <p>🧠 **Nivel Cognitivo Estimado**: {}</p>
            <button style="padding: 10px 20px; background-color: #4CAF50; color: white; border: none; cursor: pointer;" onclick="window.location.reload();">🔄 Jugar de nuevo</button>
        </div>
        """.format(corrects, total_time, nivel_cognitivo), unsafe_allow_html=True)

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

                st.session_state.current_attempt += 1
                time.sleep(1)
                load_new_question()
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)


# 🔹 Cargar la interfaz del juego
load_emotions()
