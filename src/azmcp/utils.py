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

class AdoMcp:
    
    @staticmethod
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


