import streamlit as st
import os
#from openai import OpenAI
from dotenv import load_dotenv  # Para cargar la API Key desde un archivo .env

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

def load_ia_game():
    """Carga el juego basado en IA generativa."""
    
    # Inicializar el estado de la sesión
    if 'step' not in st.session_state:
        st.session_state['step'] = 1
    if 'user_description' not in st.session_state:
        st.session_state['user_description'] = ""
    if 'generated_image' not in st.session_state:
        st.session_state['generated_image'] = ""
    if 'generated_text' not in st.session_state:
        st.session_state['generated_text'] = ""
    if 'correct_elements' not in st.session_state:
        st.session_state['correct_elements'] = ""
    if 'incorrect_elements' not in st.session_state:
        st.session_state['incorrect_elements'] = ""
    
    # 🖌️ Estilos personalizados
    st.markdown("""
        <style>
        #MainMenu, footer, header {visibility: hidden;}
        .stApp {text-align: center;}
        .stButton>button {
            width: 100%;
            height: 60px;
            font-size: 20px;
            border-radius: 10px;
            margin: 5px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🤖 Juego con IA Generativa")
    
    # Paso 1: Descripción del usuario
    if st.session_state['step'] == 1:
        st.subheader("Describe con detalle tu casa de la infancia 🏡")
        st.session_state['user_description'] = st.text_area("Escribe aquí tu recuerdo...", height=200)
        
        if st.button("Siguiente"):  
            if st.session_state['user_description'].strip():
                generate_text_and_image()  # Generar imagen y descripción con IA
                st.session_state['step'] = 2
                st.rerun()
            else:
                st.warning("Por favor, ingresa una descripción antes de continuar.")
    
    # Paso 2: Mostrar imagen y descripción generada
    elif st.session_state['step'] == 2:
        st.subheader("Hemos generado esta imagen y descripción basándonos en tu recuerdo 📸")
        
        if st.session_state['generated_image']:
            st.image(st.session_state['generated_image'], caption="Imagen generada por IA")
        else:
            st.warning("No se ha generado ninguna imagen. Revisa la consola para más detalles.")
        
        st.write("📜 **Descripción generada:**")
        if st.session_state['generated_text']:
            st.write(st.session_state['generated_text'])
        else:
            st.warning("No se ha generado ninguna descripción. Revisa la consola para más detalles.")
        
        if st.button("Siguiente"):
            st.session_state['step'] = 3
            st.rerun()
    
    # Paso 3: Comparación de detalles
    elif st.session_state['step'] == 3:
        st.subheader("Comparación de detalles 🔍")
        st.write("Escribe qué elementos recuerdas como correctos y cuáles son incorrectos en la imagen generada.")
        st.session_state['correct_elements'] = st.text_area("Elementos correctos", height=100)
        st.session_state['incorrect_elements'] = st.text_area("Elementos incorrectos o diferentes", height=100)
        
        if st.button("Finalizar"):
            # Reiniciar el juego
            st.session_state['step'] = 1
            st.session_state['user_description'] = ""
            st.session_state['generated_image'] = ""
            st.session_state['generated_text'] = ""
            st.session_state['correct_elements'] = ""
            st.session_state['incorrect_elements'] = ""
            st.session_state['page'] = 'login'  # Regresar al menú
            st.rerun()


def generate_text_and_image():
    """Genera una imagen y una descripción detallada basada en la entrada del usuario."""
    
    # Obtener la API Key desde las variables de entorno
    api_key = os.getenv("OPENAI_API_KEY")  # Clave de API de OpenAI
    if not api_key:
        st.error("⚠️ No se ha configurado una API Key. Por favor, configura la variable de entorno 'OPENAI_API_KEY' en el archivo .env.")
        return
    
    # Configurar el cliente de OpenAI
    client = OpenAI(api_key=api_key)

    # 🔹 Generar texto descriptivo con GPT
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # Puedes cambiar a "gpt-3.5-turbo" si prefieres
            messages=[
                {"role": "system", "content": "Eres un asistente útil que describe imágenes con detalle."},
                {"role": "user", "content": f"Describe una imagen detallada de: {st.session_state['user_description']}"}
            ],
            max_tokens=500,  # Límite de tokens para la descripción
            temperature=0.7,  # Control de creatividad
            stream=False
        )
        st.session_state['generated_text'] = response.choices[0].message.content
        st.success("✅ Texto generado correctamente.")
    except Exception as e:
        st.error(f"❌ Error al generar el texto: {str(e)}")
        return

    # 🔹 Generar imagen con DALL-E
    try:
        response = client.images.generate(
            model="dall-e-3",  # Modelo de DALL-E
            prompt=st.session_state['user_description'],
            n=1,  # Número de imágenes a generar
            size="1024x1024"  # Tamaño de la imagen
        )
        st.session_state['generated_image'] = response.data[0].url  # URL de la imagen generada
        st.success("✅ Imagen generada correctamente.")
    except Exception as e:
        st.error(f"❌ Error al generar la imagen: {str(e)}")