# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Button, Static, Log
from textual.reactive import reactive
from textual import events
from typing import Optional
import asyncio


class AzMCPApp(App):
    CSS_PATH = "tcss/styles.tcss"
    TITLE = "Azure DevOps MCP Server"
    SUB_TITLE = "Model Context Protocol Server for Azure DevOps"
    show_sidebar = reactive(True)
    current_view = reactive("home")
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="main"):
            with Horizontal():
                with Vertical(id="sidebar"):
                    yield Button("Home", id="home-btn", variant="primary")
                    yield Button("Work Items", id="workitems-btn")
                    yield Button("Builds", id="builds-btn")
                    yield Button("Repositories", id="repos-btn")
                    yield Button("Releases", id="releases-btn")
                    yield Button("Test Plans", id="testplans-btn")
                    yield Button("Settings", id="settings-btn")
                with Vertical(id="content"):
                    with Container(id="home-view"):
                        yield Static("# Azure DevOps MCP Server", id="title")
                        yield Static("Welcome to the Azure DevOps Model Context Protocol Server interface.", id="subtitle")
                        yield Static("This application provides a terminal user interface for interacting with Azure DevOps services", id="description")
                        with Horizontal(id="action-buttons"):
                            yield Button("Connect to Azure DevOps", id="connect-btn", variant="success")
                            yield Button("View Documentation", id="docs-btn")
        yield Footer()

    def _get_home_view(self) -> Container:
        container = Container(id="home-view")
        container.mount(Static("# Azure DevOps MCP Server", id="title"))
        container.mount(Static("Welcome to the Azure DevOps Model Context Protocol Server interface.", id="subtitle"))
        container.mount(Static("This application provides a terminal user interface for interacting with Azure DevOps services", id="description"))
        action_buttons = Horizontal(id="action-buttons")
        action_buttons.mount(Button("Connect to Azure DevOps", id="connect-btn", variant="success"))
        action_buttons.mount(Button("View Documentation", id="docs-btn"))
        container.mount(action_buttons)
        return container

    def _get_workitems_view(self) -> Container:
        container = Container(id="workitems-view")
        container.mount(Static("# Work Items", id="workitems-title"))
        container.mount(Static("Manage Azure DevOps work items", id="workitems-subtitle"))
        action_buttons = Horizontal(id="workitem-actions")
        action_buttons.mount(Button("Create Work Item", id="create-wi-btn", variant="primary"))
        action_buttons.mount(Button("Search Work Items", id="search-wi-btn"))
        action_buttons.mount(Button("My Work Items", id="my-wi-btn"))
        container.mount(action_buttons)
        container.mount(Log(id="workitems-log"))
        return container
    
    def _get_builds_view(self) -> Container:
        container = Container(id="builds-view")
        container.mount(Static("# Build Pipelines", id="builds-title"))
        container.mount(Static("Monitor and manage build pipelines", id="builds-subtitle"))
        action_buttons = Horizontal(id="build-actions")
        action_buttons.mount(Button("View Builds", id="view-builds-btn", variant="primary"))
        action_buttons.mount(Button("Queue Build", id="queue-build-btn"))
        action_buttons.mount(Button("Build History", id="build-history-btn"))
        container.mount(action_buttons)
        container.mount(Log(id="builds-log"))
        return container
    
    def _get_repos_view(self) -> Container:
        container = Container(id="repos-view")
        container.mount(Static("# Repositories", id="repos-title"))
        container.mount(Static("Manage source repositories and pull requests", id="repos-subtitle"))
        action_buttons = Horizontal(id="repo-actions")
        action_buttons.mount(Button("List Repositories", id="list-repos-btn", variant="primary"))
        action_buttons.mount(Button("Pull Requests", id="prs-btn"))
        action_buttons.mount(Button("Branches", id="branches-btn"))
        container.mount(action_buttons)
        container.mount(Log(id="repos-log"))
        return container
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        
        if button_id == "home-btn":
            self._switch_view("home")
        elif button_id == "workitems-btn":
            self._switch_view("workitems")
        elif button_id == "builds-btn":
            self._switch_view("builds")
        elif button_id == "repos-btn":
            self._switch_view("repos")
        elif button_id == "releases-btn":
            self._switch_view("releases")
        elif button_id == "testplans-btn":
            self._switch_view("testplans")
        elif button_id == "settings-btn":
            self._switch_view("settings")
        elif button_id == "connect-btn":
            self._handle_connect()
        elif button_id == "docs-btn":
            self._show_documentation()
    
    def _switch_view(self, view_name: str) -> None:
        self.current_view = view_name
        content_container = self.query_one("#content")
        content_container.remove_children()
        
        if view_name == "home":
            content_container.mount(self._get_home_view())
        elif view_name == "workitems":
            content_container.mount(self._get_workitems_view())
        elif view_name == "builds":
            content_container.mount(self._get_builds_view())
        elif view_name == "repos":
            content_container.mount(self._get_repos_view())
    
    def _handle_connect(self) -> None:
        log_widget = self._get_current_log()
        if log_widget:
            log_widget.write_line("Attempting to connect to Azure DevOps...")
            log_widget.write_line("Connection functionality will be implemented here.")
    
    def _show_documentation(self) -> None:
        log_widget = self._get_current_log()
        if log_widget:
            log_widget.write_line("Opening documentation...")
            log_widget.write_line("Documentation will be available at docs/ folder.")
    
    def _get_current_log(self) -> Optional[Log]:
        try:
            if self.current_view == "workitems":
                return self.query_one("#workitems-log", Log)
            elif self.current_view == "builds":
                return self.query_one("#builds-log", Log)
            elif self.current_view == "repos":
                return self.query_one("#repos-log", Log)
        except:
            pass
        return None


def main() -> None:
    app = AzMCPApp()
    app.run()


if __name__ == "__main__":
    main()
