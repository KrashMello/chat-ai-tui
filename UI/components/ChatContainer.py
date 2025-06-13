from textual.containers import Container
from components.ChatMessage import ChatMessage


class ChatContainer(Container):
    """Contenedor para los mensajes del chat."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_class("chat-container")
        self.can_focus = True

    def add_message(self, content: str, is_user: bool = False):
        message = ChatMessage(content, is_user)
        self.mount(message)
        self.scroll_end()
