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
    path_history,
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


def save_chat():
    global messages, provider
    name = ""
    data = {}
    data["data"] = []
    if provider == "groq":
        name = messages[0]["content"]
    if provider == "gemini":
        name = messages[0]["parts"]["text"]
    file_name = f"{name}.json"
    path_file = os.path.join(path_history, file_name)
    if not os.path.exists(path_file):
        os.makedirs(os.path.dirname(path_history), exist_ok=True)
    for message in messages:
        if provider == "groq":
            data["data"].append({message["role"]: message["content"]})
        if provider == "gemini":
            if message["role"] == "user":
                data["data"].append({message["role"]: message["parts"]["text"]})
            else:
                data["data"].append({message["role"]: message["parts"][0]["text"]})
    with open(path_file, "w") as f:
        json.dump(data, f, indent=4)


def load_chat():
    global messages
    messages = []
    files = os.listdir(path_history)
    list = []
    for i, file in enumerate(files):
        file_name = file.split(".")[0]
        list.append(f"[{i}] {file_name}")
    print("\n".join(list))
    file_selected = input("Ingresa el numero del chat: ")
    if not file_selected.isdigit():
        print("debe ingresar un numero")
        return ""
    file_selected = int(file_selected)
    if file_selected > len(files) or file_selected < 0:
        print("numero invalido")
        return ""
    file_name = files[file_selected]
    with open(os.path.join(path_history, file_name), "r") as f:
        data = json.load(f)
    for item in data["data"]:
        role = "user"
        message = ""
        for aurole, aumessage in item.items():
            role = aurole
            message = aumessage
        if provider == "groq":
            if role == "model":
                role = "assistant"
            messages.append(
                {
                    "role": role,
                    "content": message,
                }
            )
        if provider == "gemini":
            if role == "assistant":
                role = "model"
            if role == "user":
                messages.append(
                    {
                        "role": role,
                        "parts": {
                            "text": message,
                        },
                    }
                )
            else:
                messages.append(
                    {
                        "role": role,
                        "parts": [
                            {
                                "text": message,
                            }
                        ],
                    }
                )
        if role == "user":
            message = f"👤: {message}"
        else:
            message = f"🤖: {message}"
        console.print(Markdown(message))


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
                "content": f"{question}\n",
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
                    "text": f"{question}\n",
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
    print("/load: Listar los chats")
    print("/help: Mostrar este mensaje")
    print("/setApiKey: Guardar la API key")
    print("/setProvider: Cambiar el proveedor")
    print("/setUrl: Cambiar la URL del proveedor")
    print("/setModel: Cambiar el modelo del proveedor")
    print("clear: limpiar la pantalla pero mantiene la conversacion")


def clear():
    global provider, model
    os.system("cls" if os.name == "nt" else "clear")
    print("Chat AI - CLI")
    print("Version 0.2.0")
    print("Ingrese tus preguntas y recibirás respuestas")
    print("Usa el comando /help para ver los comandos disponibles")
    print(f"Usando el proveedor {provider}")
    print(f"Usando el modelo {model}")


def chat():
    global exit, provider, model, api_key, url
    clear()
    while not exit:
        question = input("👤: ")
        match question:
            case "clear":
                clear()
            case "/load":
                load_chat()
            case "/new":
                save_chat()
                reset_chat()
                clear()
            case "/exit":
                if len(messages) > 0:
                    save_chat()
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
                    console.print(Markdown(f"🤖: {message}"))
