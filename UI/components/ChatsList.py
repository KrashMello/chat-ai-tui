from components.ChatMessage import ChatMessage
from textual.containers import Container
from textual.app import ComposeResult
from textual.widgets import ListItem, Label
from textual.binding import Binding
from components.ListView import ListView

from textual import events


class ChatList(Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.add_class("chat-container")
        # self.can_focus = True

    def compose(self) -> ComposeResult:
        yield ListView(
            id="chat-list",
            *[
                ListItem(Label("Hola")),
                ListItem(Label("Hola")),
                ListItem(Label("¡Hola!")),
                ListItem(Label("¡Hola!")),
                ListItem(Label("🤖: ¡Hola!")),
                ListItem(Label("🤖: ¡Hola!")),
                ListItem(Label("✅ Hola")),
                ListItem(Label("✅ Hola")),
                ListItem(Label("Ó Hola")),
                ListItem(Label("Ó Hola")),
            ],
        )

    # def on_key(self, event: events.Key) -> None:
    #     if event.key == "j":
    #         event.prevent_default()
    #         self.focus_next()

    def add_chat(self, content: str, is_user: bool = False):
        message = ChatMessage(content, is_user)
        self.mount(message)
