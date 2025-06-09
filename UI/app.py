from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TextArea, Static
from textual.containers import Vertical, Horizontal

from textual import events
from components.ChatContainer import ChatContainer


class Main(App):
    """Textual Chat AI"""

    TITLE = ""
    CSS_PATH = "tui.css"
    BINDINGS = [
        ("t", "toggle_theme", "Cambiar Tema"),
        ("q", "quit", "Salir"),
        ("h", "help", "Ayuda"),
        ("n", "new_chat", "Nuevo Chat"),
    ]

    def compose(self) -> ComposeResult:
        """Crear widgets de la aplicación."""
        yield Header(icon="🤖", classes="header")

        # Área de contenido principal: diseño horizontal para la barra lateral y la visualización del chat
        with Horizontal(id="main-content-area"):
            # Barra lateral izquierda para el historial de chat
            # with Vertical(id="history-sidebar"):
            #     yield Static("HISTORIAL DE CHATS", classes="sidebar-title")
            #     # Entradas de chat de ejemplo, estas serían dinámicas en una aplicación real
            #     yield Static("Historial no implementado", classes="chat-entry")
            #     #yield Static("Chat 2", classes="chat-entry")

            # Área de visualización de chat principal derecha
            with Vertical(id="chat-display-area"):
                yield Static(
                    "NUEVO CHAT", classes="new-chat-title"
                )  # Título "NUEVO CHAT" del diagrama
                yield ChatContainer(id="chat-area")  # Mensajes CHAT IA

        yield TextArea(
            id="global-prompt-input",
        )

        yield Footer()

    def on_key(self, event: events.Key) -> None:
        """Manejar eventos de teclado."""
        if event.key == "ctrl+j":
            self.submit_message()
            event.prevent_default()
            # event.stop_propagation()

    def submit_message(self) -> None:
        """Enviar el mensaje actual."""
        text_area = self.query_one("#global-prompt-input", TextArea)
        if not text_area.text.strip():
            return

        chat_container = self.query_one("#chat-area", ChatContainer)
        chat_container.add_message(text_area.text, is_user=True)
        chat_container.add_message("Este es un mensaje de ejemplo del AI")

        text_area.text = ""
        text_area.focus()

    # def action_toggle_theme(self) -> None:
    #     """Cambiar entre tema claro y oscuro."""
    #     self.theme = (
    #         "textual-dark" if self.theme == "textual-light" else "textual-light"
    #     )

    # def action_help(self) -> None:
    #     """Mostrar ayuda."""
    #     self.notify(
    #         "Presiona 't' para cambiar el tema, 'q' para salir, 'n' para nuevo chat"
    #     )

    def action_new_chat(self) -> None:
        """Crear un nuevo chat."""
        chat_container = self.query_one("#chat-area", ChatContainer)
        chat_container.remove_children()
        chat_container.add_message("Nuevo chat iniciado", is_user=False)


if __name__ == "__main__":
    app = Main()
    app.run()
