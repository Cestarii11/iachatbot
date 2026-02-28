import os
import json
import base64
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'uploads'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'txt', 'mp3', 'wav', 'ogg', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_metadata(file):
    filename = secure_filename(file.filename)
    file.seek(0, 2)
    size = file.tell()
    file.seek(0)
    return {
        "name": filename,
        "size": size,
        "size_readable": f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB",
        "type": file.content_type or "unknown"
    }


def query_gemini(messages, model="gemini-2.5-flash", file_data=None):
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        # Build contents list
        contents = []

        # Add previous conversation history
        for msg in messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))

        # Build current user message parts
        current_parts = []

        # Add images if present
        if file_data:
            for fd in file_data:
                if fd["type"].startswith("image/"):
                    current_parts.append(
                        types.Part(inline_data=types.Blob(
                            mime_type=fd["type"],
                            data=base64.b64decode(fd["b64"])
                        ))
                    )

        # Add text
        user_text = messages[-1]["content"] if messages else ""
        current_parts.append(types.Part(text=user_text))
        contents.append(types.Content(role="user", parts=current_parts))

        # Generate — strip "models/" prefix if present
        model_id = model.replace("models/", "")

        response = client.models.generate_content(
            model=model_id,
            contents=contents,
            config=types.GenerateContentConfig(max_output_tokens=2048)
        )

        reply_text = response.text

        # Token usage
        try:
            input_tokens  = response.usage_metadata.prompt_token_count
            output_tokens = response.usage_metadata.candidates_token_count
            total_tokens  = response.usage_metadata.total_token_count
        except Exception:
            input_tokens  = len(user_text.split()) * 2
            output_tokens = len(reply_text.split()) * 2
            total_tokens  = input_tokens + output_tokens

        return {
            "reply": reply_text,
            "tokens": {"input": input_tokens, "output": output_tokens, "total": total_tokens},
            "model": model_id, "provider": "Google Gemini"
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        provider = request.form.get('provider', 'gemini')
        model    = request.form.get('model', '')
        messages = json.loads(request.form.get('messages', '[]'))

        file_data, file_metadata = [], []
        for file in request.files.getlist('files'):
            if file and file.filename and allowed_file(file.filename):
                meta = get_file_metadata(file)
                file_metadata.append(meta)
                file_data.append({
                    "name": meta["name"],
                    "type": meta["type"],
                    "b64": base64.b64encode(file.read()).decode('utf-8')
                })

        if provider == 'gemini':
            result = query_gemini(messages, model or 'gemini-2.5-flash', file_data or None)
        else:
            result = {"error": f"Proveedor '{provider}' no soportado."}

        if "error" in result:
            return jsonify({"success": False, "error": result["error"]}), 500

        return jsonify({
            "success": True,
            "reply":    result.get("reply", ""),
            "tokens":   result.get("tokens", {}),
            "model":    result.get("model", ""),
            "provider": result.get("provider", ""),
            "files":    file_metadata
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    available = {}
    if os.getenv("GEMINI_API_KEY"):
        available["gemini"] = [
            "gemini-2.0-flash",
            "gemini-2.0-flash-lite",
            "gemini-2.5-flash",
            "gemini-2.5-pro",
        ]
    return jsonify(available)

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, port=5000)
