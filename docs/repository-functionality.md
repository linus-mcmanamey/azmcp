# Repository Functionality

## Overview
The `azmcp` application automatically detects the repository from which it is called and provides Azure DevOps repository management functionality.

## Features

### Automatic Repository Detection
- Detects Azure DevOps repositories in various URL formats:
  - SSH: `git@ssh.dev.azure.com:v3/{org}/{project}/{repo}`
  - HTTPS: `https://dev.azure.com/{org}/{project}/_git/{repo}`
  - VSTS: `https://{org}.visualstudio.com/{project}/_git/{repo}`

### Repository Status Display
When switching to the Repositories tab, the application shows:
- Current working directory
- Repository name, project, and organization
- Current branch
- Repository type (Azure DevOps or other)

### Pull Request Creation
The "Create PR" button automatically:
1. Gets the current branch
2. Determines the default branch (usually 'main')
3. Validates there are commits to create a PR for
4. Creates a pull request using the Azure DevOps MCP server
5. Provides feedback on success or failure

### Other Repository Operations
- **List Repositories**: Shows all repositories in the project
- **Pull Requests**: Lists existing pull requests for the current repository
- **Branches**: Shows all branches in the current repository

## Usage

1. Navigate to any Azure DevOps repository on your local machine
2. Run `azmcp` from within that repository directory
3. Switch to the "Repositories" tab
4. Use the provided buttons to manage your repository

## Requirements

- Must be run from within a git repository
- Repository must be hosted on Azure DevOps
- Azure CLI authentication must be configured
- Azure DevOps PAT token must be available in environment variables
