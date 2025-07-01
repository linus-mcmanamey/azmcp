# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, Log
from textual.app import ComposeResult


class SettingsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Static("# Settings", id="settings-title"),
            Static("Configure Azure DevOps connection and application settings", id="settings-subtitle"),
            Horizontal(
                Button("Connection Settings", id="connection-settings-btn", variant="primary"),
                Button("UI Settings", id="ui-settings-btn"),
                Button("Reset Settings", id="reset-settings-btn"),
                id="settings-actions"
            ),
            Log(id="settings-log"),
            id="settings-container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        log_widget = self.query_one("#settings-log", Log)
        
        if event.button.id == "connection-settings-btn":
            log_widget.write_line("Opening connection settings...")
        elif event.button.id == "ui-settings-btn":
            log_widget.write_line("Opening UI settings...")
        elif event.button.id == "reset-settings-btn":
            log_widget.write_line("Resetting settings...")
