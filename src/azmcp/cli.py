# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

import sys
import argparse
from typing import List, Optional
from .app import AzMCPApp


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

For more information, visit: https://github.com/linus-mcmanamey/azmcp
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.0.1"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )
    
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)
    
    try:
        app = AzMCPApp()
        if args.debug:
            app.debug = True
        app.run()
        return 0
    except KeyboardInterrupt:
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
