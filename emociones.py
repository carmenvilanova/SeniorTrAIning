import streamlit as st
import random
import time

# 🔹 Cargar datos del juego
def load_game_data():
    return {
        "Feliz": "https://www.lavanguardia.com/files/image_449_220/uploads/2016/03/29/5fa2bd2401a8c.jpeg",
        "Triste": "https://img.freepik.com/fotos-premium/retrato-mujer-expresion-triste_641386-636.jpg",
        "Enojado": "https://image.jimcdn.com/app/cms/image/transf/dimension=410x1024:format=jpg/path/s667233d5fec7d9ab/image/idb79a0f9233d354a/version/1527621370/image.jpg",
        "Sorprendido": "https://media.istockphoto.com/id/1392578709/es/foto/tipo-afroamericano-conmocionado-mirando-hacia-otro-lado-con-expresi%C3%B3n-de-asombro.jpg?s=612x612&w=0&k=20&c=3sBViaSFcdU32rNQO4tt23L8fDrtExmt9r255DHnbdU="
    }

# 🔹 Guardar respuestas
def save_response(user_choice, correct_answer):
    if "responses" not in st.session_state:
        st.session_state.responses = []
    st.session_state.responses.append({
        "Elección del usuario": user_choice,
        "Respuesta correcta": correct_answer,
        "Resultado": "Correcto" if user_choice == correct_answer else "Incorrecto"
    })
    if user_choice == correct_answer:
        st.session_state.correct_answers += 1  # Sumar acierto

# 🔹 Cargar nueva pregunta
def load_new_question():
    st.session_state.correct_answer, st.session_state.img_url = random.choice(list(st.session_state.game_data.items()))
    st.session_state.selected_option = None
    st.session_state.start_time_question = time.time()  # Guardar tiempo de inicio para esta pregunta

# 🔹 Iniciar juego
def init_game():
    if "game_data" not in st.session_state:
        st.session_state.game_data = load_game_data()
        st.session_state.current_attempt = 0
        st.session_state.correct_answers = 0
        st.session_state.start_time = time.time()  # Guardar inicio de tiempo
        st.session_state.start_time_question = time.time()  # Guardar inicio de la primera pregunta
        load_new_question()

# 🔹 Diseño centrado
def add_styles():
    st.markdown(
        """
        <style>
        .center {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .stButton>button {
            width: 200px;
            height: 50px;
            font-size: 18px;
            margin: 5px;
        }
        .stImage>img {
            display: block;
            margin: 0 auto;
            width: 300px;  /* Tamaño fijo */
            height: 300px;  /* Tamaño fijo */
            object-fit: cover;  /* Ajusta la imagen para que no se deforme */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# 🔹 Mostrar temporizador en tiempo real
def display_timer():
    # Mostrar tiempo en tiempo real
    elapsed_time = time.time() - st.session_state.start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    return f"{minutes:02}:{seconds:02}"

# 🔹 Cargar juego
def load_emotions():
    init_game()
    add_styles()

    st.markdown("<div class='center'>", unsafe_allow_html=True)
    st.title("🎭 Juego de Identificación de Emociones 🎭")

    # 📌 Mostrar intento actual (1/10, 2/10, etc.)
    if st.session_state.current_attempt <= 10:
        st.subheader(f"Ronda {st.session_state.current_attempt}/10")

    # 📌 Temporizador en tiempo real (se actualiza constantemente)
    timer_placeholder = st.empty()
    timer_placeholder.text(f"⏱️ Tiempo: {display_timer()}")  # Mostrar temporizador en tiempo real

    if st.session_state.current_attempt > 10:
        # ⏳ Mostrar resultados finales
        total_time = round(time.time() - st.session_state.start_time, 2)
        st.success(f"🎉 ¡Felicidades! Has completado el juego.")
        st.write(f"✅ Aciertos: {st.session_state.correct_answers}/10")
        st.write(f"⏳ Tiempo total: {total_time} segundos")

        # 🔄 Botones para reiniciar y volver al menú
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Jugar de nuevo"):
                del st.session_state["game_data"]
                del st.session_state["responses"]
                st.rerun()
        with col2:
            if st.button("Volver al Menú"):
                st.session_state['page'] = 'login'  # Cambia la página a 'home'
                st.rerun()  # Recargar la aplicación para volver al menú
    
        st.write("---")
    else:
        st.image(st.session_state.img_url, caption="¿Qué emoción ves en la imagen?", width=300)
        st.write("### Elige una opción:")

        # Respuestas fijas (solo se cargan una vez)
        cols = st.columns(2)
        for i, option in enumerate(st.session_state.game_data.keys()):
            with cols[i % 2]:
                if st.button(option, key=option):
                    st.session_state.selected_option = option
                    save_response(option, st.session_state.correct_answer)

                    # Calcular tiempo transcurrido de esta pregunta
                    question_time = round(time.time() - st.session_state.start_time_question, 2)

                    if option == st.session_state.correct_answer:
                        st.success(f"¡Correcto! 🏆 (Tiempo de respuesta: {question_time} segundos)")
                    else:
                        st.error(f"❌ Incorrecto. La respuesta correcta era: {st.session_state.correct_answer} (Tiempo de respuesta: {question_time} segundos)")

                    # Incrementar ronda solo después de responder
                    st.session_state.current_attempt += 1
                    time.sleep(1)  # Pausa antes de la siguiente pregunta
                    load_new_question()
                    st.rerun()

        # 🛑 Botón de salida del juego (centrado)
        if st.button("Salir del juego"):
            st.session_state['page'] = 'login'  # Cambia la página a 'home'
            st.rerun()  # Recargar la aplicación para volver al menú

    st.write("</div>", unsafe_allow_html=True)

# 🔹 Cargar la interfaz del juego
load_emotions()
