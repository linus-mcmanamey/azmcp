# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, TabbedContent, TabPane, Static
from textual.reactive import reactive
from typing import Optional

from .screens import HomeScreen, WorkItemsScreen, BuildsScreen, RepositoriesWidget, ReleasesScreen, TestPlansScreen, SettingsScreen


class AzMCPApp(App):
    CSS_PATH = "tcss/styles.tcss"
    TITLE = "Azure DevOps MCP Server"
    SUB_TITLE = "Model Context Protocol Server for Azure DevOps"
    
    SCREENS = {
        "home": HomeScreen,
        "workitems": WorkItemsScreen,
        "builds": BuildsScreen,
        "repositories": RepositoriesWidget,
        "releases": ReleasesScreen,
        "testplans": TestPlansScreen,
        "settings": SettingsScreen,
    }
    
    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="home-tab"):
            with TabPane("Home", id="home-tab"):
                yield Static("Welcome to Azure DevOps MCP Server")
            with TabPane("Work Items", id="workitems-tab"):
                yield Static("Work Items content coming soon")
            with TabPane("Builds", id="builds-tab"):
                yield Static("Builds content coming soon")
            with TabPane("Repositories", id="repositories-tab"):
                yield RepositoriesWidget()
            with TabPane("Releases", id="releases-tab"):
                yield Static("Releases content coming soon")
            with TabPane("Test Plans", id="testplans-tab"):
                yield Static("Test Plans content coming soon")
            with TabPane("Settings", id="settings-tab"):
                yield Static("Settings content coming soon")
        yield Footer()
    
    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        # No need for screen switching since widgets are mounted directly in tabs
        pass


def main() -> None:
    app = AzMCPApp()
    app.run()


if __name__ == "__main__":
    main()
