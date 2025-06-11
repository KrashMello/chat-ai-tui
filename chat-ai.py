#!/usr/bin/python3
import os
import signal
import sys
from dotenv import load_dotenv

from module.chat import chat, save_chat

load_dotenv()


def main():
    os.system("cls" if os.name == "nt" else "clear")
    chat()


def handler(sig, frame):
    save_chat()
    print("\nPrograma terminado con Ctrl+C")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    main()
