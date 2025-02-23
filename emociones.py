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

    st.title("🎭 Juego de Identificación de Emociones 🎭")

    if st.session_state.current_attempt <= 10:
        st.subheader(f"Ronda {st.session_state.current_attempt}/10")

    if st.session_state.current_attempt > 10:
        total_time = round(time.time() - st.session_state.start_time, 2)
        
        # 📌 Preparar datos para ML
        corrects = st.session_state.correct_answers
        avg_reaction_time = sum([resp["Tiempo de reacción"] for resp in st.session_state.responses]) / 10

        df = pd.DataFrame([[corrects, avg_reaction_time]], columns=["Aciertos", "Tiempo de reacción"])
        
        # 📌 Predecir con el modelo
        nivel_cognitivo = st.session_state.ml_model.predict(df)[0]
        
        st.success("🎉 ¡Juego Completado!")
        st.write(f"✅ Aciertos: {corrects}/10")
        st.write(f"⏳ Tiempo total: {total_time} segundos")
        st.write(f"🧠 **Nivel Cognitivo Estimado**: {nivel_cognitivo}")

        if st.button("🔄 Jugar de nuevo"):
            del st.session_state["game_data"]
            del st.session_state["responses"]
            st.rerun()
    
    else:
        st.image(st.session_state.img_url, caption="¿Qué emoción ves en la imagen?", width=300)
        st.write("### Elige una opción:")

        cols = st.columns(2)
        for i, option in enumerate(st.session_state.game_data.keys()):
            with cols[i % 2]:
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

# 🔹 Cargar la interfaz del juego
load_emotions()
