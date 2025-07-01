# SPDX-FileCopyrightText: 2025-present U.N. Owen <'linus.mcmanamey@dpfem.tas.gov.au'>
#
# SPDX-License-Identifier: MIT

from .__about__ import __version__
from .app import AzMCPApp, main
from .cli import main as cli_main

__all__ = ["__version__", "AzMCPApp", "main", "cli_main"]
