#!/usr/bin/env python3
import os
import subprocess
import sys
import typer
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
from dotenv import load_dotenv
from icecream import ic

load_dotenv()


def call_ado_mcp_server(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    org = os.getenv("AZURE_DEVOPS_ORG", "emstas")
    url = os.getenv("AZURE_DEVOPS_ORG_URL", f"https://dev.azure.com/{org}")
    project = os.getenv("AZURE_DEVOPS_PROJECT", "Program Unify")
    request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool_name, "arguments": arguments}}
    try:
        cmd = ["npx", "-y", "@azure-devops/mcp", org]
        env = os.environ.copy()
        env.update({"AZURE_DEVOPS_PAT": os.getenv("AZURE_DEVOPS_PAT", ""), "AZURE_DEVOPS_ORG_URL": url, "AZURE_DEVOPS_PROJECT": project})
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env)
        stdout, stderr = process.communicate(json.dumps(request) + "\n", timeout=30)
        ic(stdout)
        if process.returncode == 0:
            lines = stdout.strip().split("\n")
            for line in lines:
                if line.strip() and not line.startswith("Azure DevOps MCP Server"):
                    try:
                        response = json.loads(line)
                        return response
                    except json.JSONDecodeError:
                        continue
        return {"error": f"MCP server error: {stderr}"}
    except Exception as e:
        return {"error": str(e)}


def run_script_with_help_fallback(script_name: str, args: List[str], command_path: str, command_name: Optional[str] = None) -> bool:
    try:
        script_path = Path(__file__).parent / "scripts" / script_name
        cmd = [sys.executable, str(script_path)] + args
        result = subprocess.run(cmd, capture_output=False, text=True)
        if result.returncode != 0:
            if command_name:
                typer.echo(f"Command failed. Try 'azmcp {command_path} {command_name} --help' for usage information")
            else:
                typer.echo(f"Command failed. Try 'azmcp {command_path} --help' for usage information")
            return False
        return True
    except Exception as e:
        typer.echo(f"Error running script {script_name}: {e}")
        if command_name:
            typer.echo(f"Try 'azmcp {command_path} {command_name} --help' for usage information")
        else:
            typer.echo(f"Try 'azmcp {command_path} --help' for usage information")
        return False


def handle_command_failure(command_path: str, command_name: str, message: str = "Command failed") -> None:
    typer.echo(message)
    typer.echo(f"Try 'azmcp {command_path} {command_name} --help' for usage information")
