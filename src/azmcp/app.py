# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, TabbedContent, TabPane
from textual.reactive import reactive
from typing import Optional

from .screens import HomeScreen, WorkItemsScreen, BuildsScreen, RepositoriesScreen, ReleasesScreen, TestPlansScreen, SettingsScreen


class AzMCPApp(App):
    CSS_PATH = "tcss/styles.tcss"
    TITLE = "Azure DevOps MCP Server"
    SUB_TITLE = "Model Context Protocol Server for Azure DevOps"
    
    SCREENS = {
        "home": HomeScreen,
        "workitems": WorkItemsScreen,
        "builds": BuildsScreen,
        "repositories": RepositoriesScreen,
        "releases": ReleasesScreen,
        "testplans": TestPlansScreen,
        "settings": SettingsScreen,
    }
    
    def compose(self) -> ComposeResult:
        yield Header()
        with TabbedContent(initial="home-tab"):
            with TabPane("Home", id="home-tab"):
                yield Container(id="home-content")
            with TabPane("Work Items", id="workitems-tab"):
                yield Container(id="workitems-content")
            with TabPane("Builds", id="builds-tab"):
                yield Container(id="builds-content")
            with TabPane("Repositories", id="repositories-tab"):
                yield Container(id="repositories-content")
            with TabPane("Releases", id="releases-tab"):
                yield Container(id="releases-content")
            with TabPane("Test Plans", id="testplans-tab"):
                yield Container(id="testplans-content")
            with TabPane("Settings", id="settings-tab"):
                yield Container(id="settings-content")
        yield Footer()
    
    def on_tabbed_content_tab_activated(self, event: TabbedContent.TabActivated) -> None:
        tab_id = event.tab.id
        if tab_id:
            screen_name = tab_id.replace("-tab", "")
            if screen_name in self.SCREENS:
                self.switch_screen(screen_name)


def main() -> None:
    app = AzMCPApp()
    app.run()


if __name__ == "__main__":
    main()
