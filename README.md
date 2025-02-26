# 🚀 SeniorTrAIning
Repositorio para el desarrollo del proyecto **SeniorTrAIning** dentro del hackathon de **OdiseIA4Good**.

## 📌 Líneas de trabajo
El proyecto se divide en dos principales líneas de trabajo:

1. **Demo de la aplicación con Streamlit** 📲  
   * Responsables: *Carmen y Nacho*
2. **Generación de datos sintéticos y modelo de clasificación del nivel de deterioro cognitivo** 🧠  
   * Responsables: *Camilo y Óscar*

---

## ⚙️ Configuración de la base de datos
⚠️ **Importante:** Asegúrate de tener Python instalado antes de ejecutar la configuración de la base de datos.

Para configurar la base de datos, ejecuta el siguiente comando:

```bash
python database_setup.py
```

> 📝 **Nota:** Verifica que todas las dependencias necesarias estén instaladas.

---
## 🔑 Configuración del archivo .env
Para que la aplicación funcione correctamente, es necesario configurar un archivo ``` .env ``` con la API Key de OpenAI. Sigue estos pasos:

1. Crea un archivo ``` .env ``` en la raíz del proyecto.

2. Añade la API Key de OpenAI en el archivo ``` .env ``` de la siguiente manera:

```bash 
OPENAI_API_KEY=sk-tu_clave_api_aquí
```
> 📝 **Nota:** Reemplaza ``` sk-tu_clave_api_aquí ``` con tu clave API de OpenAI. Si no tienes una, regístrate en OpenAI y genera una clave.
3. Guarda el archivo. Asegúrate de que el archivo ``` .env ``` no se suba al repositorio (está incluido en ``` .gitignore ``` por defecto).

---

## 🚀 Ejecutar la aplicación
Para iniciar la aplicación con Streamlit, usa el siguiente comando:

```bash
streamlit run app.py
```

> 🔥 **Tip:** Si tienes problemas al ejecutar la aplicación, revisa que tengas todas las librerías necesarias instaladas con `pip install -r requirements.txt`.

---

## ⚠️ Advertencias y Recomendaciones
⚠️ **Caution:** Asegúrate de trabajar en un entorno virtual para evitar conflictos de dependencias.

💡 **Recomendación:** Utiliza `venv` o `conda` para gestionar los paquetes de Python y evitar problemas con las versiones de las librerías.

```bash
# Crear un entorno virtual con venv
test -d venv || python -m venv venv
source venv/bin/activate  # En macOS/Linux
venv\Scripts\activate     # En Windows
```

---

✨ ¡Colaboremos juntos para hacer de **SeniorTrAIning** un gran proyecto! 🚀

