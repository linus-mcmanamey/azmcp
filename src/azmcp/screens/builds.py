# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, Log
from textual.app import ComposeResult


class BuildsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Static("# Build Pipelines", id="builds-title"),
            Static("Monitor and manage build pipelines", id="builds-subtitle"),
            Horizontal(
                Button("View Builds", id="view-builds-btn", variant="primary"),
                Button("Queue Build", id="queue-build-btn"),
                Button("Build History", id="build-history-btn"),
                id="build-actions"
            ),
            Log(id="builds-log"),
            id="builds-container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        log_widget = self.query_one("#builds-log", Log)
        
        if event.button.id == "view-builds-btn":
            log_widget.write_line("Loading current builds...")
        elif event.button.id == "queue-build-btn":
            log_widget.write_line("Queueing new build...")
        elif event.button.id == "build-history-btn":
            log_widget.write_line("Loading build history...")
