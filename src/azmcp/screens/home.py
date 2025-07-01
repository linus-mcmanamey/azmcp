# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, Log
from textual.app import ComposeResult


class HomeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Static("# Azure DevOps MCP Server", id="title"),
            Static("Welcome to the Azure DevOps Model Context Protocol Server interface.", id="subtitle"),
            Static("This application provides a terminal user interface for interacting with Azure DevOps services", id="description"),
            Static("Authentication Status: Authenticated", id="auth-status"),
            Horizontal(
                Button("Connect to Azure DevOps", id="connect-btn", variant="success"),
                Button("View Documentation", id="docs-btn"),
                id="action-buttons"
            ),
            Log(id="main-log"),
            id="home-container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "connect-btn":
            self._handle_connect()
        elif event.button.id == "docs-btn":
            self._show_documentation()
    
    def _handle_connect(self) -> None:
        log_widget = self.query_one("#main-log", Log)
        log_widget.write_line("Attempting to connect to Azure DevOps...")
        log_widget.write_line("Connection functionality will be implemented here.")
    
    def _show_documentation(self) -> None:
        log_widget = self.query_one("#main-log", Log)
        log_widget.write_line("Opening documentation...")
        log_widget.write_line("Documentation will be available at docs/ folder.")
