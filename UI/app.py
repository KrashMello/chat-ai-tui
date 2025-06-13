from components.ChatsList import ChatList
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static
from textual.containers import Vertical, Horizontal
from components.TextArea import TextArea

from textual import events
from components.ChatContainer import ChatContainer
from components.ListView import ListView


class Main(App):
    TITLE = ""
    CSS_PATH = "tui.css"
    BINDINGS = [
        ("t", "toggle_theme", "Cambiar Tema"),
        ("q", "quit", "Salir"),
        ("?", "help", "Ayuda"),
        ("n", "new_chat", "Nuevo Chat"),
    ]

    def compose(self) -> ComposeResult:
        with Horizontal(id="main-content-area"):
            with Vertical(id="history-sidebar"):
                yield Static("HISTORIAL DE CHATS")
                yield ChatList()

            with Vertical(id="chat-display-area"):
                yield Static("CHAT", classes="new-chat-title")
                yield ChatContainer(id="chat-area")

        yield TextArea(id="global-prompt-input")

    def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            event.prevent_default()
            self.submit_message()
            # event.stop_propagation()
        if event.key == "i":
            event.prevent_default()
            text_area = self.query_one("#global-prompt-input", TextArea)
            text_area.focus()
        if event.key == "escape":
            event.prevent_default()
            self.screen.focus_next()
        if event.key == "ctrl+l":
            event.prevent_default()
            chat_list = self.query_one("#chat-list", ListView)
            chat_list.focus()

    def submit_message(self) -> None:
        text_area = self.query_one("#global-prompt-input", TextArea)
        if not text_area.text.strip():
            return

        chat_container = self.query_one("#chat-area", ChatContainer)
        chat_container.add_message(text_area.text, is_user=True)
        chat_container.add_message("Este es un mensaje de ejemplo del AI")

        text_area.text = ""

    # def action_toggle_theme(self) -> None:
    #     """Cambiar entre tema claro y oscuro."""
    #     self.theme = (
    #         "textual-dark" if self.theme == "textual-light" else "textual-light"
    #     )

    def action_help(self) -> None:
        self.notify(
            "Presiona 't' para cambiar el tema, 'q' para salir, 'n' para nuevo chat"
        )

    def action_new_chat(self) -> None:
        chat_container = self.query_one("#chat-area", ChatContainer)
        chat_container.remove_children()
        chat_container.add_message("Nuevo chat iniciado", is_user=False)


if __name__ == "__main__":
    app = Main()
    app.run()
