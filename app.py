import streamlit as st
import random
import pandas as pd

def load_game_data():
    return {
        "Feliz": "https://www.lavanguardia.com/files/image_449_220/uploads/2016/03/29/5fa2bd2401a8c.jpeg",
        "Triste": "https://img.freepik.com/fotos-premium/retrato-mujer-expresion-triste_641386-636.jpg",
        "Enojado": "https://image.jimcdn.com/app/cms/image/transf/dimension=410x1024:format=jpg/path/s667233d5fec7d9ab/image/idb79a0f9233d354a/version/1527621370/image.jpg",
        "Sorprendido": "https://media.istockphoto.com/id/1392578709/es/foto/tipo-afroamericano-conmocionado-mirando-hacia-otro-lado-con-expresi%C3%B3n-de-asombro.jpg?s=612x612&w=0&k=20&c=3sBViaSFcdU32rNQO4tt23L8fDrtExmt9r255DHnbdU="
    }

def save_response(user_choice, correct_answer):
    if "responses" not in st.session_state:
        st.session_state.responses = []
    st.session_state.responses.append({
        "Elección del usuario": user_choice,
        "Respuesta correcta": correct_answer,
        "Resultado": "Correcto" if user_choice == correct_answer else "Incorrecto"
    })

def export_to_excel():
    if "responses" in st.session_state and st.session_state.responses:
        df = pd.DataFrame(st.session_state.responses)
        df.to_excel("respuestas.xlsx", index=False)
        st.success("¡Respuestas guardadas en respuestas.xlsx!")

def load_new_question():
    st.session_state.correct_answer, st.session_state.img_url = random.choice(list(st.session_state.game_data.items()))
    st.session_state.options = list(st.session_state.game_data.keys())
    random.shuffle(st.session_state.options)
    st.session_state.selected_option = None

def main():
    st.title("Juego de Identificación de Emociones")
    st.write("Selecciona la opción que mejor describe la emoción en la imagen.")
    
    if "game_data" not in st.session_state:
        st.session_state.game_data = load_game_data()
        load_new_question()
    
    st.image(st.session_state.img_url, caption="¿Qué emoción ves en la imagen?", width=300)
    
    st.write("### Elige una opción:")
    
    cols = st.columns(2)
    for i, option in enumerate(st.session_state.options):
        with cols[i % 2]:
            if st.button(option, key=option):
                st.session_state.selected_option = option
                save_response(option, st.session_state.correct_answer)
                
                if option == st.session_state.correct_answer:
                    st.success("¡Correcto! 🏆")
                else:
                    st.error(f"Incorrecto. La respuesta correcta era: {st.session_state.correct_answer}")
                
                load_new_question()
                st.rerun()
    
    st.write("---")
    if st.button("Exportar respuestas a Excel"):
        export_to_excel()

if __name__ == "__main__":
    main()
