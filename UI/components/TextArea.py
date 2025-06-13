from textual import events
from textual.app import App, ComposeResult
from textual.widgets import TextArea as TA


class TextArea(TA):
    """A subclass of TextArea with parenthesis-closing functionality."""

    def _on_key(self, event: events.Key) -> None:
        if event.character == "(":
            self.insert("()")
            self.move_cursor_relative(columns=-1)
            event.prevent_default()
        # if event.key == "escape":
        #     self.screen.focus_next()
        #     event.prevent_default()
