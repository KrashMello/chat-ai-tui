import toml
import os
from dotenv import load_dotenv

load_dotenv()
HOME_DIR = os.path.expanduser("~")


def get_ia_config(type: str):
    try:
        with open(HOME_DIR + "/.config/chat-ai/config.toml", "r") as archivo:
            configuracion = toml.load(archivo)
        provider = configuracion["global"]["provider"]

        if type == "PROVIDER":
            return provider
        else:
            return configuracion[provider][type]
    except Exception as e:
        print("Error al cargar la configuración:", str(e))
