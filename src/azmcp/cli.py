# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

import sys
import argparse
from typing import List, Optional
from .app import AzMCPApp
from .aure_login import AzureLogin
from pathlib import Path

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="azmcp",
        description="Azure DevOps Model Context Protocol Server Terminal Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
                Examples:
                azmcp                    # Launch the interactive terminal interface
                azmcp --version          # Show version information
                azmcp --help             # Show this help message
                For more information, visit: https://github.com/linus-mcmanamey/azmcp """)
    parser.add_argument("--version", action="version", version="%(prog)s 0.0.1")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    sys.path.append(str(Path(__file__).parent.parent))
    sys.path.append("src")  # Ensure src is in the path for module imports
    parser = create_parser()
    args = parser.parse_args(argv)
    
    # Handle Azure authentication before starting the app
    azure_login = AzureLogin()
    print("Checking Azure CLI authentication...")
    
    if not azure_login.check_azure_login():
        print("Azure CLI authentication required.")
        if not azure_login.ensure_azure_login():
            print("Authentication failed. Exiting.", file=sys.stderr)
            return 1
        print("Authentication successful!")
    else:
        print("Already authenticated with Azure CLI.")
    
    try:
        app = AzMCPApp()
        app.run()
        return 0
    except KeyboardInterrupt:
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
