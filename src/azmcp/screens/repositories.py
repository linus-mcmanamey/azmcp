# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, Log
from textual.app import ComposeResult


class RepositoriesScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Static("# Repositories", id="repos-title"),
            Static("Manage source repositories and pull requests", id="repos-subtitle"),
            Horizontal(
                Button("List Repositories", id="list-repos-btn", variant="primary"),
                Button("Pull Requests", id="prs-btn"),
                Button("Branches", id="branches-btn"),
                id="repo-actions"
            ),
            Log(id="repos-log"),
            id="repos-container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        log_widget = self.query_one("#repos-log", Log)
        
        if event.button.id == "list-repos-btn":
            log_widget.write_line("Loading repositories...")
        elif event.button.id == "prs-btn":
            log_widget.write_line("Loading pull requests...")
        elif event.button.id == "branches-btn":
            log_widget.write_line("Loading branches...")
