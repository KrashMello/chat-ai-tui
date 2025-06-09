#!/usr/bin/python3
import os
import signal
import sys
from dotenv import load_dotenv

from module.chat import chat

load_dotenv()


def main():
    os.system("cls" if os.name == "nt" else "clear")
    chat()


def handler(sig, frame):
    print("\nPrograma terminado con Ctrl+C")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    main()
