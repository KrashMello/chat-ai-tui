import subprocess
import os
import requests
import json
import threading
import signal
import sys
from time import sleep
from pynput import keyboard as kb

URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"
API_KEY = os.environ.get("GROQ_API_KEY")
messages = []
exit = False


def reset_chat():
    global messages
    messages = []  # Limpiamos el messages


def ask():
    global messages
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
    if response.status_code != 200:
        print("Error:", response.status_code)
        return ""
    data = response.json()
    response = data["choices"][0]["message"]["content"]
    messages.append(data["choices"][0]["message"])
    return response


def help():
    print("Comandos disponibles:")
    print("/new: Reinicia el chat")
    print("/exit: Salir del chat")
    print("/help: Mostrar este mensaje")


def main():
    os.system("clear")
    global exit
    while not exit:
        question = input("> ")
        match question:
            case "/new":
                reset_chat()
                os.system("clear")
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
                echo = subprocess.Popen(["echo", message], stdout=subprocess.PIPE)
                glow = subprocess.Popen(
                    ["glow", "-"], stdin=echo.stdout, stdout=sys.stdout
                )
                echo.stdout.close()
                threading.Timer(0.3, lambda: [echo.kill(), glow.kill()]).start()
                glow.wait()


def handler(sig, frame):
    print("\nPrograma terminado con Ctrl+C")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    main()
