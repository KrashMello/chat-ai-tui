debemos crear un arcchivo de configuracion para el chat-ai
en la ruta ~/.config/chat-ai/config.toml
```toml
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
```
por ahora solo tenemos compatibilidad con el api de groq y gemini
