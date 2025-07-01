# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, Log
from textual.app import ComposeResult


class ReleasesScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Static("# Releases", id="releases-title"),
            Static("Manage release pipelines and deployments", id="releases-subtitle"),
            Horizontal(
                Button("View Releases", id="view-releases-btn", variant="primary"),
                Button("Create Release", id="create-release-btn"),
                Button("Release History", id="release-history-btn"),
                id="release-actions"
            ),
            Log(id="releases-log"),
            id="releases-container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        log_widget = self.query_one("#releases-log", Log)
        
        if event.button.id == "view-releases-btn":
            log_widget.write_line("Loading current releases...")
        elif event.button.id == "create-release-btn":
            log_widget.write_line("Creating new release...")
        elif event.button.id == "release-history-btn":
            log_widget.write_line("Loading release history...")
