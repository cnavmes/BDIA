import os
from dotenv import load_dotenv
from langchain_google_community import GmailToolkit
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from pydantic import BaseModel, Field
from typing import List, Type
from langchain_google_community.gmail.send_message import GmailSendMessage
from langchain_google_community.gmail.base import GmailBaseTool
import feedparser
from langchain.tools import BaseTool


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
email_to = os.getenv("EMAIL_TO", "cristobal.navas.mesa.alu@iesfernandoaguilar.es")
email_subject = "Noticias y eventos Cádiz"

if not api_key:
    raise ValueError("Falta GEMINI_API_KEY en .env")

# Inicializa LLM Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

# Gmail toolkit
gmail_toolkit = GmailToolkit()

# Define a fixed schema for send_gmail_message
class FixedSendMessageSchema(BaseModel):
    """Input schema for `FixedGmailSendMessageTool`."""
    message: str = Field(
        ...,
        description="The message to send.",
    )
    to: List[str] = Field(
        ...,
        description="The list of recipients.",
    )
    subject: str = Field(
        ...,
        description="The subject of the message.",
    )

# Create a custom tool that uses the fixed schema
class FixedGmailSendMessageTool(GmailSendMessage):
    name: str = "send_gmail_message"
    description: str = (
        "Use this tool to send email messages. The input is the message, recipients"
    )
    args_schema: Type[FixedSendMessageSchema] = FixedSendMessageSchema

# Get the API resource from the original toolkit to pass to our fixed tool
gmail_api_resource = gmail_toolkit.api_resource

# Instantiate our fixed tool
fixed_send_gmail_message_tool = FixedGmailSendMessageTool(api_resource=gmail_api_resource)

# DuckDuckGo herramienta
duckduckgo_tool = DuckDuckGoSearchRun()

# RSS reader tool (personalizada)
class RSSReaderTool(BaseTool):
    name: str = "rss_reader"
    description: str = "Obtiene y resume las noticias desde una URL RSS indicada. Incluye los títulos, resúmenes y enlaces HTML de las noticias."

    def _run(self, rss_url: str) -> str:
        feed = feedparser.parse(rss_url)
        results = []
        for entry in feed.entries[:5]:
            title = entry.title
            link = entry.link
            summary = entry.summary if hasattr(entry, "summary") else ""
            results.append(f"<li><strong>{title}</strong>: {summary} <a href='{link}'>Leer más</a></li>")
        return "<ul>" + "".join(results) + "</ul>"

    def _arun(self, *args, **kwargs):
        raise NotImplementedError("RSS reader no soporta async.")


rss_tool = RSSReaderTool()

# Todas las herramientas disponibles para el agente
tools = [fixed_send_gmail_message_tool, duckduckgo_tool, rss_tool]
agent_executor = create_agent(llm, tools)

def main():
    print("Buscando, generando y enviando email automáticamente...")

    example_query = (
        f"Recopila las últimas noticias sobre Cádiz usando: "
        f"1) DuckDuckGo y "
        f"2) la herramienta 'rss_reader' con el feed 'https://www.diariodecadiz.es/rss' y 'https://www.lavozdigital.es/rss/2.0/provincia/cadiz'. "
        f"Redacta un resumen estructurado en HTML para enviar por email, siguiendo este formato: "
        f"- Introducción breve. "
        f"- Lista de noticias principales (título, breve explicación y enlace de la fuente). "
        f"- Conclusión/llamada a seguir informado. "
        f"Presenta todo en HTML usando <h2> para el título principal, <ul>/<li> para la lista y <a href=''> para los enlaces."
        f"Usa 'send_gmail_message' para enviar el email a ['{email_to}'] con asunto '{email_subject}' y el resumen como cuerpo."
    )

    events = agent_executor.stream(
        {"messages": [("user", example_query)]},
        stream_mode="values"
    )

    for event in events:
        print("Evento recibido del agente:")
        if "messages" in event:
            print(event["messages"][-1].content)
        else:
            print(event)

if __name__ == "__main__":
    main()
