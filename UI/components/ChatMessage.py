from textual.widgets import Markdown
import os


class ChatMessage(Markdown):
    """Widget para mostrar un mensaje individual del chat."""

    def __init__(self, content: str, is_user: bool = False):
        username = os.environ.get("USERNAME")  # Para Windows
        if not username:
            username = os.environ.get("USER")  # Para Linux/macOS
        super().__init__(f"{username}: {content}" if is_user else f"🤖: {content}")
        self.is_user = is_user
        self.add_class("user-message" if is_user else "ai-message")
