import toml
import os
from dotenv import load_dotenv

load_dotenv()
HOME_DIR = os.path.expanduser("~")
providers = ["groq", "gemini"]
DEFAULT_CONFIG = """
[global]
provider="gemini"
theme="nord"
[groq]
URL="https://api.groq.com/openai/v1/chat/completions"
MODEL="llama-3.3-70b-versatile"
API_KEY="api_key"
[gemini]
URL="https://generativelanguage.googleapis.com/v1beta/models"
MODEL="gemini-2.0-flash"
API_KEY="api_key"
"""

PATH_CONFIG = HOME_DIR + "/.config/chat-ai/config.toml"

PATH_HISTORY = HOME_DIR + "/.config/chat-ai/history/"
VERSION = "Experimental 0.2.1"


def get_ia_config(type: str):
    if os.path.exists(PATH_CONFIG):
        try:
            with open(PATH_CONFIG, "r") as archivo:
                configuracion = toml.load(archivo)
            provider = configuracion["global"]["provider"]

            if type == "PROVIDER":
                return provider
            else:
                return configuracion[provider][type]
        except Exception as e:
            print("Error al cargar la configuración:", str(e))
    else:
        try:
            os.makedirs(os.path.dirname(PATH_CONFIG), exist_ok=True)
            with open(PATH_CONFIG, "w") as archivo:
                toml.dump(toml.loads(DEFAULT_CONFIG), archivo)

            with open(PATH_CONFIG, "r") as archivo:
                configuracion = toml.load(archivo)

            provider = configuracion["global"]["provider"]

            if type == "PROVIDER":
                return provider
            else:
                return configuracion[provider][type]
        except Exception as e:
            print("Error al cargar la configuración:", str(e))


def set_config_provider_api_key(provider: str, api_key: str):
    try:
        with open(PATH_CONFIG, "r") as archivo:
            configuracion = toml.load(archivo)
        configuracion[provider]["API_KEY"] = api_key
        with open(PATH_CONFIG, "w") as archivo:
            toml.dump(configuracion, archivo)
    except Exception as e:
        print("Error al cargar la configuración:", str(e))


def set_config_provider(provider: str):
    global providers
    try:
        if provider not in providers:
            print(f"los proveedores disponibles son: {', '.join(providers)}")
            return None
        else:
            with open(PATH_CONFIG, "r") as archivo:
                configuracion = toml.load(archivo)
            configuracion["global"]["provider"] = provider
            with open(PATH_CONFIG, "w") as archivo:
                toml.dump(configuracion, archivo)
            return True
    except Exception as e:
        print("Error al cargar la configuración:", str(e))


def set_config_provider_url(provider: str, url: str):
    try:
        with open(PATH_CONFIG, "r") as archivo:
            configuracion = toml.load(archivo)
        configuracion[provider]["URL"] = url
        with open(PATH_CONFIG, "w") as archivo:
            toml.dump(configuracion, archivo)
    except Exception as e:
        print("Error al cargar la configuración:", str(e))


def set_config_provider_model(provider: str, model: str):
    try:
        with open(PATH_CONFIG, "r") as archivo:
            configuracion = toml.load(archivo)
        configuracion[provider]["MODEL"] = model
        with open(PATH_CONFIG, "w") as archivo:
            toml.dump(configuracion, archivo)
    except Exception as e:
        print("Error al cargar la configuración:", str(e))
