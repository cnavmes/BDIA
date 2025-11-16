import requests
import chromadb
from chromadb.config import Settings
from config import CHUNKS_OUTPUT

LLM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

def search_relevant_docs(query_text, top_k=3):
    client = chromadb.PersistentClient(path=CHUNKS_OUTPUT, settings=Settings())
    collection = client.get_or_create_collection("normativa_andalucia")
    results = collection.query(
        query_texts=[query_text],
        n_results=top_k,
        include=["documents", "metadatas"] 
    )
    return results["documents"][0]

def call_llm_studio(prompt: str):
    response = requests.post(LLM_STUDIO_API_URL, json={
        "model": "gemma-3-12b",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 768,  
        "temperature": 0.7,
        "top_p": 0.9,      
        "frequency_penalty": 0,
        "presence_penalty": 0
    })
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def generate_answer(user_question):
    relevant_docs = search_relevant_docs(user_question)
    context = "\n\n".join(relevant_docs)
    prompt = f"Usa esta información para responder la pregunta:\n{context}\n\nPregunta: {user_question}\nRespuesta:"
    answer = call_llm_studio(prompt)
    return answer

if __name__ == "__main__":
    pregunta = "Tengo un hijo con TEA,¿que procedimiento debo seguir?"
    respuesta = generate_answer(pregunta)
    print("Respuesta generada:\n", respuesta)
