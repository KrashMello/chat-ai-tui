from textual.containers import Container
from components.ChatMessage import ChatMessage


class ChatContainer(Container):
    """Contenedor para los mensajes del chat."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_class("chat-container")

    def add_message(self, content: str, is_user: bool = False):
        """Agregar un nuevo mensaje al chat."""
        message = ChatMessage(content, is_user)
        self.mount(message)
        self.scroll_end()
