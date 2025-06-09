import subprocess
import os
import requests
import json
import threading
import sys
from time import sleep
from module.config import (
    get_ia_config,
    set_config_provider,
    set_config_provider_api_key,
    set_config_provider_model,
    set_config_provider_url,
)
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


def ask(question):
    global api_key, provider, url, model
    global messages

    if not api_key:
        print("Por favor, configura la API_KEY con el comando /setApiKey")
        return ""
    if not question:
        print(
            "no se pudo generar la respuesta debido a que no se ha ingresado una pregunta"
        )
        return ""
    if not provider:
        print("Por favor, configura el proveedor con el comando /setProvider")
        return ""

    URL = ""
    headers = {
        "Content-Type": "application/json",
    }
    body = None

    if provider == "groq":
        URL = url if url is not None else ""
        headers["Authorization"] = f"Bearer {api_key}"
        body = {
            "model": model,
            "messages": messages,
        }
        messages.append(
            {
                "role": "user",
                "content": question,
            }
        )
    if provider == "gemini":
        URL = f"{url}/{model}:generateContent?key={api_key}" if url is not None else ""
        body = {
            "contents": messages,
        }
        messages.append(
            {
                "role": "user",
                "parts": {
                    "text": question,
                },
            }
        )

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
    print("/setApiKey: Guardar la API key")
    print("/setProvider: Cambiar el proveedor")
    print("/setUrl: Cambiar la URL del proveedor")
    print("/setModel: Cambiar el modelo del proveedor")
    print("clear: limpiar la pantalla pero mantiene la conversacion")


def clear():
    global provider, model
    os.system("cls" if os.name == "nt" else "clear")
    print("Chat AI - Tui")
    print("Ingrese tus preguntas y recibirás respuestas")
    print("Usa el comando /help para ver los comandos disponibles")
    print(f"Usando el proveedor {provider}")
    print(f"Usando el modelo {model}")


def chat():
    global exit, provider, model, api_key, url
    clear()
    while not exit:
        question = input("> ")
        match question:
            case "clear":
                clear()
            case "/new":
                reset_chat()
                clear()
            case "/exit":
                exit = True
            case "/help":
                help()
            case "/setApiKey":
                api_key = input("Ingrese la API key: ")
                set_config_provider_api_key(
                    provider if provider is not None else "groq", api_key
                )
                api_key = get_ia_config("API_KEY")
                print("API key guardada")
            case "/setProvider":
                sprovider = input("Ingrese el proveedor: ")
                seter = set_config_provider(sprovider)
                if seter is not None:
                    provider = get_ia_config("PROVIDER")
                    api_key = get_ia_config("API_KEY")
                    url = get_ia_config("URL")
                    model = get_ia_config("MODEL")
                    reset_chat()
                    clear()
                    print("Proveedor guardado")
            case "/setUrl":
                url = input("Ingrese la URL del proveedor: ")
                set_config_provider_url(
                    provider if provider is not None else "groq", url
                )
                url = get_ia_config("URL")
                print("URL guardada")
            case "/setModel":
                model = input("Ingrese el modelo del proveedor: ")
                set_config_provider_model(
                    provider if provider is not None else "groq", model
                )
                model = get_ia_config("MODEL")
                print("Modelo guardado")
            case _:
                message = ask(question)
                if message:
                    console.print(Markdown(message))
