# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from textual.widget import Widget
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static, Button, Log
from textual.app import ComposeResult
import subprocess
import os
from pathlib import Path
from ..utils import AdoMcp


class RepositoriesWidget(Widget):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sidebar_items = [
            "Current Repository",
            "Pull Requests", 
            "Branches",
            "Recent Activity",
            "Repository Settings"
        ]
    
    def compose(self) -> ComposeResult:
        yield Container(
            Horizontal(
                Vertical(
                    Static("Repository Navigation", id="sidebar-title"),
                    Button("Current Repository", id="sidebar-current-repo"),
                    Button("Pull Requests", id="sidebar-prs"),
                    Button("Branches", id="sidebar-branches"),
                    Button("Recent Activity", id="sidebar-activity"),
                    Button("Repository Settings", id="sidebar-settings"),
                    id="sidebar"
                ),
                Vertical(
                    Static("# Repositories", id="repos-title"),
                    Static("Manage source repositories and pull requests", id="repos-subtitle"),
                    Horizontal(
                        Button("List Repositories", id="list-repos-btn", variant="primary"),
                        Button("Pull Requests", id="prs-btn"),
                        Button("Branches", id="branches-btn"),
                        Button("Create PR", id="create-pr-btn", variant="success"),
                        id="repo-actions"
                    ),
                    Log(id="repos-log"),
                    id="main-content"
                ),
                id="main-container"
            ),
            id="repos-container"
        )
    
    def on_mount(self) -> None:
        try:
            log_widget = self.query_one("#repos-log", Log)
            self._show_repository_status(log_widget)
        except Exception:
            pass  # Log widget not found, widget may not be fully mounted yet
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        log_widget = self.query_one("#repos-log", Log)
        
        # Handle main action buttons
        if event.button.id == "list-repos-btn":
            self._list_repositories(log_widget)
        elif event.button.id == "prs-btn":
            self._list_pull_requests(log_widget)
        elif event.button.id == "branches-btn":
            self._list_branches(log_widget)
        elif event.button.id == "create-pr-btn":
            self._create_pull_request(log_widget)
        
        # Handle sidebar buttons
        elif event.button.id == "sidebar-current-repo":
            self._show_repository_status(log_widget)
        elif event.button.id == "sidebar-prs":
            self._list_pull_requests(log_widget)
        elif event.button.id == "sidebar-branches":
            self._list_branches(log_widget)
        elif event.button.id == "sidebar-activity":
            log_widget.write_line("Loading recent repository activity...")
            log_widget.write_line("Recent activity functionality will be implemented here")
        elif event.button.id == "sidebar-settings":
            log_widget.write_line("Repository settings...")
            log_widget.write_line("Repository settings functionality will be implemented here")
    
    def _get_current_repository_info(self) -> tuple[str, str, str]:
        try:
            current_dir = Path.cwd()
            result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, cwd=current_dir)
            if result.returncode != 0:
                return "", "", ""
            
            remote_url = result.stdout.strip()
            
            # Handle Azure DevOps URLs
            if "dev.azure.com" in remote_url or "visualstudio.com" in remote_url:
                # SSH format: git@ssh.dev.azure.com:v3/{org}/{project}/{repo}
                if "@ssh.dev.azure.com:v3" in remote_url:
                    path_part = remote_url.split("@ssh.dev.azure.com:v3/")[1]
                    parts = path_part.split("/")
                    org = parts[0]
                    project = parts[1]
                    repo = parts[2].replace(".git", "") if len(parts) > 2 else ""
                
                # HTTPS format: https://dev.azure.com/{org}/{project}/_git/{repo}
                elif "https://dev.azure.com" in remote_url:
                    path_part = remote_url.replace("https://dev.azure.com/", "")
                    parts = path_part.split("/")
                    org = parts[0]
                    project = parts[1]
                    repo = parts[3].replace(".git", "") if len(parts) > 3 and parts[2] == "_git" else ""
                
                # Old VSTS format: https://{org}.visualstudio.com/{project}/_git/{repo}
                elif "visualstudio.com" in remote_url:
                    if "https://" in remote_url:
                        path_part = remote_url.replace("https://", "").split("/")
                        org = path_part[0].split(".")[0]
                        project = path_part[1] if len(path_part) > 1 else ""
                        repo = path_part[3].replace(".git", "") if len(path_part) > 3 and path_part[2] == "_git" else ""
                    else:
                        return "", "", ""
                
                else:
                    return "", "", ""
                
                return org, project, repo
            
            return "", "", ""
        except Exception:
            return "", "", ""
    
    def _get_current_branch(self) -> str:
        try:
            result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, cwd=Path.cwd())
            return result.stdout.strip() if result.returncode == 0 else ""
        except Exception:
            return ""
    
    def _get_default_branch(self, repository_id: str) -> str:
        try:
            response = AdoMcp.call_ado_mcp_server("mcp_ado_repo_get_repo_by_name_or_id", {"project": os.getenv("AZURE_DEVOPS_PROJECT", ""), "repositoryNameOrId": repository_id})
            if "result" in response and "content" in response["result"]:
                for item in response["result"]["content"]:
                    if item.get("type") == "text" and "defaultBranch" in item.get("text", ""):
                        text = item["text"]
                        if "refs/heads/" in text:
                            return text.split("refs/heads/")[1].split("\\n")[0].strip()
            return "main"
        except Exception:
            return "main"
    
    def _list_repositories(self, log_widget: Log) -> None:
        log_widget.write_line("Loading repositories...")
        try:
            response = AdoMcp.call_ado_mcp_server("mcp_ado_repo_list_repos_by_project", {"project": os.getenv("AZURE_DEVOPS_PROJECT", "")})
            if "result" in response and "content" in response["result"]:
                log_widget.write_line("Repositories:")
                for item in response["result"]["content"]:
                    if item.get("type") == "text":
                        log_widget.write_line(item["text"])
            else:
                log_widget.write_line(f"Error loading repositories: {response.get('error', 'Unknown error')}")
        except Exception as e:
            log_widget.write_line(f"Error: {str(e)}")
    
    def _list_pull_requests(self, log_widget: Log) -> None:
        log_widget.write_line("Loading pull requests...")
        try:
            org, project, repo = self._get_current_repository_info()
            if not repo:
                log_widget.write_line("Not in a valid Azure DevOps repository")
                return
            
            response = AdoMcp.call_ado_mcp_server("mcp_ado_repo_list_pull_requests_by_repo", {"repositoryId": repo})
            if "result" in response and "content" in response["result"]:
                log_widget.write_line("Pull Requests:")
                for item in response["result"]["content"]:
                    if item.get("type") == "text":
                        log_widget.write_line(item["text"])
            else:
                log_widget.write_line(f"Error loading pull requests: {response.get('error', 'Unknown error')}")
        except Exception as e:
            log_widget.write_line(f"Error: {str(e)}")
    
    def _list_branches(self, log_widget: Log) -> None:
        log_widget.write_line("Loading branches...")
        try:
            org, project, repo = self._get_current_repository_info()
            if not repo:
                log_widget.write_line("Not in a valid Azure DevOps repository")
                return
            
            response = AdoMcp.call_ado_mcp_server("mcp_ado_repo_list_branches_by_repo", {"repositoryId": repo})
            if "result" in response and "content" in response["result"]:
                log_widget.write_line("Branches:")
                for item in response["result"]["content"]:
                    if item.get("type") == "text":
                        log_widget.write_line(item["text"])
            else:
                log_widget.write_line(f"Error loading branches: {response.get('error', 'Unknown error')}")
        except Exception as e:
            log_widget.write_line(f"Error: {str(e)}")
    
    def _create_pull_request(self, log_widget: Log) -> None:
        log_widget.write_line("Creating pull request for current branch...")
        try:
            org, project, repo = self._get_current_repository_info()
            current_branch = self._get_current_branch()
            
            log_widget.write_line(f"Repository: {repo} (Project: {project}, Org: {org})")
            
            if not repo:
                log_widget.write_line("Error: Not in a valid Azure DevOps repository or could not parse repository info")
                log_widget.write_line("Ensure you are in an Azure DevOps git repository")
                return
            
            if not current_branch:
                log_widget.write_line("Error: Could not determine current branch")
                return
            
            default_branch = self._get_default_branch(repo)
            log_widget.write_line(f"Current branch: {current_branch}")
            log_widget.write_line(f"Target branch: {default_branch}")
            
            if current_branch == default_branch:
                log_widget.write_line(f"Error: Cannot create PR from {default_branch} to itself")
                log_widget.write_line("Please switch to a feature branch first")
                return
            
            # Check if there are any commits to create PR for
            try:
                result = subprocess.run(["git", "rev-list", "--count", f"{default_branch}..{current_branch}"], capture_output=True, text=True, cwd=Path.cwd())
                if result.returncode == 0 and result.stdout.strip() == "0":
                    log_widget.write_line(f"Error: No commits found between {current_branch} and {default_branch}")
                    log_widget.write_line("Make sure you have committed changes on this branch")
                    return
            except Exception:
                pass  # Continue anyway if we can't check commits
            
            source_ref = f"refs/heads/{current_branch}"
            target_ref = f"refs/heads/{default_branch}"
            title = f"PR from {current_branch} to {default_branch}"
            description = f"Automated pull request created from branch {current_branch}"
            
            pr_args = {"repositoryId": repo, "sourceRefName": source_ref, "targetRefName": target_ref, "title": title, "description": description}
            
            log_widget.write_line("Submitting pull request...")
            response = AdoMcp.call_ado_mcp_server("mcp_ado_repo_create_pull_request", pr_args)
            
            if "result" in response and "content" in response["result"]:
                log_widget.write_line("Pull request created successfully!")
                for item in response["result"]["content"]:
                    if item.get("type") == "text":
                        log_widget.write_line(item["text"])
            else:
                log_widget.write_line(f"Error creating pull request: {response.get('error', 'Unknown error')}")
                
        except Exception as e:
            log_widget.write_line(f"Error: {str(e)}")
    
    def _show_repository_status(self, log_widget: Log) -> None:
        try:
            current_dir = Path.cwd()
            log_widget.write_line(f"Current working directory: {current_dir}")
            
            org, project, repo = self._get_current_repository_info()
            current_branch = self._get_current_branch()
            
            if repo:
                log_widget.write_line(f"Azure DevOps Repository: {repo}")
                log_widget.write_line(f"Project: {project}")
                log_widget.write_line(f"Organization: {org}")
                if current_branch:
                    log_widget.write_line(f"Current branch: {current_branch}")
                else:
                    log_widget.write_line("Could not determine current branch")
            else:
                log_widget.write_line("Not in an Azure DevOps repository")
                # Check if it's any git repository
                try:
                    result = subprocess.run(["git", "status"], capture_output=True, text=True, cwd=current_dir)
                    if result.returncode == 0:
                        log_widget.write_line("This is a git repository but not Azure DevOps")
                    else:
                        log_widget.write_line("Not a git repository")
                except Exception:
                    log_widget.write_line("Not a git repository")
            
            log_widget.write_line("---")
        except Exception as e:
            log_widget.write_line(f"Error checking repository status: {str(e)}")
            log_widget.write_line("---")


# Backwards compatibility alias
RepositoriesScreen = RepositoriesWidget
