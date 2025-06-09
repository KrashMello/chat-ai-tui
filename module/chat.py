import subprocess
import os
import requests
import json
import threading
import sys
from time import sleep
from module.config import get_ia_config
from rich.console import Console
from rich.markdown import Markdown

messages = []
exit = False
console = Console()
provider = get_ia_config("PROVIDER")
api_key = get_ia_config("API_KEY")
url = get_ia_config("URL")
model = get_ia_config("MODEL")


def reset_chat():
    global messages
    messages = []  # Limpiamos el messages


def ask():
    global api_key, provider, url, model
    global messages
    if not api_key:
        print("\nError: No se encontró la API key de Groq")
        print("Por favor, configura la variable de entorno GROQ_API_KEY")
        print("En Windows puedes usar: set GROQ_API_KEY=tu-api-key")
        return ""

    URL = ""
    headers = {
        "Content-Type": "application/json",
    }
    body = None
    match provider:
        case "groq":
            URL = url if url is not None else ""
            headers["Authorization"] = f"Bearer {api_key}"
            body = {
                "model": model,
                "messages": messages,
            }
        case "gemini":
            URL = (
                f"{url}/{model}:generateContent?key={api_key}"
                if url is not None
                else ""
            )
            body = {
                "contents": messages,
            }
        case _:
            URL = url if url is not None else ""
            headers["Authorization"] = f"Bearer {api_key}"
            body = {
                "model": model,
                "messages": messages,
            }

    try:
        response = requests.post(URL, headers=headers, data=json.dumps(body))
        if response.status_code == 401:
            print("\nError: API key inválida o no autorizada")
            print("Por favor, verifica que tu API key sea correcta")
            return ""
        elif response.status_code != 200:
            print(f"\nError: {response.status_code}")
            print(response.text)
            return ""
        json_response = response.json()
        match provider:
            case "groq":
                response = json_response["choices"][0]["message"]["content"]
                messages.append(json_response["choices"][0]["message"])
            case "gemini":
                response = json_response["candidates"][0]["content"]["parts"][0]["text"]
                messages.append(json_response["candidates"][0]["content"])
            case _:
                response = json_response["choices"][0]["message"]["content"]
                messages.append(json_response["choices"][0]["message"])
        return response
    except requests.exceptions.RequestException as e:
        print(f"\nError de conexión: {str(e)}")
        return ""


def help():
    print("Comandos disponibles:")
    print("/new: Reinicia el chat")
    print("/exit: Salir del chat")
    print("/help: Mostrar este mensaje")


def chat():
    global exit, provider
    while not exit:
        question = input("> ")
        match question:
            case "/new":
                reset_chat()
                os.system("cls" if os.name == "nt" else "clear")
            case "/exit":
                exit = True
            case "/help":
                help()
            case _:
                match provider:
                    case "groq":
                        messages.append(
                            {
                                "role": "user",
                                "content": question,
                            }
                        )
                    case "gemini":
                        messages.append(
                            {
                                "role": "user",
                                "parts": {
                                    "text": question,
                                },
                            }
                        )
                    case _:
                        messages.append(
                            {
                                "role": "user",
                                "content": question,
                            }
                        )
                message = ask()
                if message:
                    console.print(Markdown(message))
