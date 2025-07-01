# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, Log
from textual.app import ComposeResult


class WorkItemsScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Static("# Work Items", id="workitems-title"),
            Static("Manage Azure DevOps work items", id="workitems-subtitle"),
            Horizontal(
                Button("Create Work Item", id="create-wi-btn", variant="primary"),
                Button("Search Work Items", id="search-wi-btn"),
                Button("My Work Items", id="my-wi-btn"),
                id="workitem-actions"
            ),
            Log(id="workitems-log"),
            id="workitems-container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        log_widget = self.query_one("#workitems-log", Log)
        
        if event.button.id == "create-wi-btn":
            log_widget.write_line("Creating new work item...")
        elif event.button.id == "search-wi-btn":
            log_widget.write_line("Searching work items...")
        elif event.button.id == "my-wi-btn":
            log_widget.write_line("Loading my work items...")
