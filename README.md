# ✦ NeuralChat — AI Chatbot Interface

Interfaz de chatbot inteligente con soporte para OpenAI y Google Gemini, renderizado de código, gestión de tokens y temas personalizables.

---

## 🚀 Instalación y puesta en marcha

### 1. Clona el proyecto o copia los archivos

```bash
mkdir neuralchat && cd neuralchat
```

### 2. Crea un entorno virtual e instala dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Configura tus API Keys

```bash
cp .env.example .env
```

Edita `.env` y añade tus claves:
```env
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
```

### 4. Inicia el servidor

```bash
python app.py
```

Abre tu navegador en **http://localhost:5000**

---

## 📁 Estructura del proyecto

```
neuralchat/
├── app.py               # Backend Flask (API + servidor)
├── requirements.txt     # Dependencias Python
├── .env.example         # Plantilla de variables de entorno
├── .env                 # Tu archivo de claves (NO subir a git)
├── uploads/             # Carpeta temporal de archivos subidos
└── templates/
    └── index.html       # Frontend completo (HTML/CSS/JS)
```

---

## ✨ Características

| Característica | Detalle |
|---|---|
| **Proveedores AI** | OpenAI (GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5) |
| | Google Gemini (1.5-flash, 1.5-pro, pro) |
| **Renderizado de código** | Bloques formateados con Highlight.js + botón copiar |
| **Gestión de tokens** | Conteo por mensaje (Input/Output/Total) en sidebar |
| **Temas** | 4 paletas: Oscuro, Claro, Aurora, Ember |
| **Archivos soportados** | Imágenes (JPG, PNG, GIF, WebP), PDFs, TXT, Audio |
| **Seguridad** | API Keys solo en backend via `.env` |

---

## 🎨 Temas disponibles

- **Oscuro** — Fondo profundo con acentos violeta
- **Claro** — Interfaz luminosa para uso diurno
- **Aurora** — Tonos teal sobre negro marino
- **Ember** — Cálidos naranjas sobre fondo oscuro

---

## 🔒 Seguridad

- Las API Keys **nunca** se exponen al frontend
- Los archivos subidos son procesados en memoria y no se persisten
- Usa HTTPS en producción (con Nginx + SSL o similar)

---

## 📦 Dependencias principales

- **Flask** — Servidor web backend
- **openai** — SDK oficial de OpenAI
- **google-generativeai** — SDK oficial de Google Gemini
- **tiktoken** — Conteo de tokens (OpenAI)
- **Pillow** — Procesamiento de imágenes para Gemini
- **Highlight.js** — Renderizado de código en frontend
