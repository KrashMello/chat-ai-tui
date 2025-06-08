#!/usr/bin/python3
import subprocess
import os
import requests
import json
import threading
import signal
import sys
from time import sleep
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv()

URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"
API_KEY = os.getenv("GROQ_API_KEY")
messages = []
exit = False
console = Console()


def reset_chat():
    global messages
    messages = [] 


def ask():
    global messages
    if not API_KEY:
        print("\nError: No se encontró la API key de Groq")
        print("Por favor, configura la variable de entorno GROQ_API_KEY")
        print("En Windows puedes usar: set GROQ_API_KEY=tu-api-key")
        return ""
        
    try:
        response = requests.post(
            URL,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
            data=json.dumps(
                {
                    "model": MODEL,
                    "messages": messages,
                }
            ),
        )
        if response.status_code == 401:
            print("\nError: API key inválida o no autorizada")
            print("Por favor, verifica que tu API key sea correcta")
            return ""
        elif response.status_code != 200:
            print(f"\nError: {response.status_code}")
            print(response.text)
            return ""
            
        data = response.json()
        response = data["choices"][0]["message"]["content"]
        messages.append(data["choices"][0]["message"])
        return response
    except requests.exceptions.RequestException as e:
        print(f"\nError de conexión: {str(e)}")
        return ""


def help():
    print("Comandos disponibles:")
    print("/new: Reinicia el chat")
    print("/exit: Salir del chat")
    print("/help: Mostrar este mensaje")


def main():
    os.system("cls" if os.name == "nt" else "clear")
    global exit
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
                messages.append(
                    {
                        "role": "user",
                        "content": question,
                    }
                )
                message = ask()
                if message:
                    console.print(Markdown(message))


def handler(sig, frame):
    print("\nPrograma terminado con Ctrl+C")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    main()
