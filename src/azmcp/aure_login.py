import subprocess
import json
from typing import Optional
from icecream import ic
from loguru import logger


class AzureLogin():

    def check_azure_login(self) -> bool:
        try:
            result = subprocess.run(["az", "account", "show"], capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False


    def ensure_azure_login(self) -> bool:
        """Ensure user is logged into Azure CLI, prompt if not"""
        if self.check_azure_login():
            return True
        logger.info("Azure CLI authentication required. Please authenticate to continue...")
        try:
            result = subprocess.run(["az", "login", "--allow-no-subscriptions", "--use-device-code"], timeout=300)
            ic(result)
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            logger.error("Authentication timeout. Please try again.")
            return False
        except KeyboardInterrupt:
            logger.exception("\nAuthentication cancelled.")
            return False


    def get_current_azure_account(self) -> Optional[dict]:
        """Get current Azure account information"""
        if not self.check_azure_login():
            return None
        try:
            result = subprocess.run(["az", "account", "show"], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError):
            pass
        return None
