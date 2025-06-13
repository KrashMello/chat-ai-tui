from textual.app import ComposeResult
from textual.widgets import ListView as LV
from textual.binding import Binding


class ListView(LV):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    BINDINGS = [
        Binding("enter", "select_cursor", "Select", show=False),
        Binding("k", "cursor_up", "Cursor up", show=False),
        Binding("j", "cursor_down", "Cursor down", show=False),
    ]
