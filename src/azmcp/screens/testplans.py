# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from textual.screen import Screen
from textual.containers import Container, Horizontal
from textual.widgets import Static, Button, Log
from textual.app import ComposeResult


class TestPlansScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Container(
            Static("# Test Plans", id="testplans-title"),
            Static("Manage test plans and test execution", id="testplans-subtitle"),
            Horizontal(
                Button("View Test Plans", id="view-testplans-btn", variant="primary"),
                Button("Create Test Plan", id="create-testplan-btn"),
                Button("Test Results", id="test-results-btn"),
                id="testplan-actions"
            ),
            Log(id="testplans-log"),
            id="testplans-container"
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        log_widget = self.query_one("#testplans-log", Log)
        
        if event.button.id == "view-testplans-btn":
            log_widget.write_line("Loading test plans...")
        elif event.button.id == "create-testplan-btn":
            log_widget.write_line("Creating new test plan...")
        elif event.button.id == "test-results-btn":
            log_widget.write_line("Loading test results...")
