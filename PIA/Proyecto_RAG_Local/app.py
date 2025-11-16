import logging
import threading
from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import chromadb
from chromadb.config import Settings
from config import CHUNKS_OUTPUT
from src.extrae_texto import main as extract_main
from src.limpia_texto import main as clean_main
from src.chunk import main as chunk_main
from src.embed_text import main as embed_main


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'clave-segura-para-session'

LLM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

def search_relevant_docs_with_meta(query_text, top_k=3):
    client = chromadb.PersistentClient(path=CHUNKS_OUTPUT, settings=Settings())
    collection = client.get_or_create_collection("normativa_andalucia")
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k,
        include=["documents", "metadatas"]
    )
    return [
        {"document": doc, "metadata": meta}
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]

def call_llm_studio(prompt: str):
    response = requests.post(LLM_STUDIO_API_URL, json={
        "model": "gemma-3-12b",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 768,
        "temperature": 0.7,
    })
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

@app.route("/", methods=["GET", "POST"])
def home():
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        if "reset" in request.form:
            session["chat_history"] = []
            return redirect(url_for("home"))

        question = request.form["question"]
        docs_meta = search_relevant_docs_with_meta(question)
        context = "\n\n".join([d["document"] for d in docs_meta])
        prompt = f"Eres un técnico especializado en TEA, responde a la pregunta de una manera cercana. Usa esta información para responder la pregunta:\n{context}\n\nPregunta: {question}\nRespuesta:"
        answer = call_llm_studio(prompt)

        session["chat_history"].append({"role": "user", "content": question})
        session["chat_history"].append({
            "role": "bot",
            "content": answer,
            "sources": docs_meta
        })

    return render_template_string('''
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Chat RAG con LM Studio</title>
<script src="https://cdn.tailwindcss.com"></script>

<script>
  window.onload = function() {
    var chatBox = document.getElementById("chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
  }
  document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("form").addEventListener("submit", function() {
      document.getElementById("loading").style.display = "block";
    });
  });
</script>
</head>
<body class="bg-gray-900 text-gray-200">
  <div class="max-w-3xl mx-auto p-6 flex flex-col h-screen">
    <h1 class="text-center text-3xl font-semibold text-blue-400 mb-6">Chat RAG con LM Studio</h1>
    <div id="chat-box" class="flex-grow overflow-y-auto p-4 bg-gray-800 rounded-lg shadow-lg mb-4">
      {% for msg in session.get("chat_history", []) %}
        <div class="mb-4 {{ 'text-right' if msg.role == 'user' else 'text-left' }}">
          <div class="inline-block p-3 rounded-lg {{ 'bg-blue-600' if msg.role == 'user' else 'bg-gray-700' }} max-w-[80%] break-words">
            <strong>{{ 'Tú:' if msg.role == 'user' else 'Bot:' }}</strong>
            <div class="whitespace-pre-wrap mt-1">{{ msg.content }}</div>
            {% if msg.role == 'bot' and msg.sources %}
              <div class="mt-3 text-sm text-blue-300">
                <b>Fuentes relevantes:</b>
                <ul class="list-disc list-inside">
                  {% for src in msg.sources %}
                    <li><i>{{ src.metadata.source }}</i>: "{{ src.document[:150] }}..."</li>
                  {% endfor %}
                </ul>
              </div>
            {% endif %}
          </div>
        </div>
      {% endfor %}
    </div>
    <div id="loading" class="text-blue-400 italic mb-2 hidden">Procesando...</div>
    <form method="post" class="flex flex-col space-y-3">
      <textarea name="question" required placeholder="Escribe tu pregunta aquí..." rows="4" class="resize-none p-3 rounded-lg bg-gray-700 text-gray-200 focus:outline-none"></textarea>
      <div class="flex space-x-3">
        <button type="submit" class="flex-grow bg-blue-600 hover:bg-blue-700 py-3 rounded-lg font-semibold transition duration-200">Enviar</button>
        <button type="submit" name="reset" value="true" class="bg-red-600 hover:bg-red-700 py-3 px-6 rounded-lg font-semibold transition duration-200">Limpiar chat</button>
      </div>
    </form>
  </div>
  <script>
    // mostrar y ocultar loading
    document.querySelector('form').addEventListener('submit', () => {
      document.getElementById('loading').classList.remove('hidden');
    });
  </script>
</body>
</html>
''')

def start_flask():
    app.run(debug=True, use_reloader=False)

def main_pipeline():
    logging.info("Inicio del pipeline de procesamiento RAG")
    extract_main()
    clean_main()
    chunk_main()
    embed_main()
    logging.info("Pipeline completado con éxito")

if __name__ == "__main__":
    main_pipeline()
    threading.Thread(target=start_flask).start()
