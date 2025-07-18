import base64
import hashlib
import hmac
import secrets
import time
import urllib3
import re
from typing import Optional
from constants import SMSGLOBAL_API_KEY, SMSGLOBAL_API_SECRET, SMSGLOBAL_API_URL

import requests

# Disable insecure HTTPS warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SMSSender:
    def __init__(self, message_template: str) -> None:
        self.message_template = message_template

    def replace_keywords(self, account_no: str, ar_balance: str, customer_name: Optional[str] = None) -> str:
        # Look for ar_balance formulas in the template, e.g., ar_balance*1.015, ar_balance+5
        def compute_formula(match):
            expr = match.group(0)
            try:
                allowed_names = {"ar_balance": float(ar_balance)}
                value = eval(expr, {"__builtins__": {}}, allowed_names)
                value = round(value + 1e-8, 2)  # round to nearest hundredths, avoid float issues
                return f"{value:.2f}"
            except Exception:
                return str(ar_balance)

        # Replace formulas first
        formula_pattern = r"ar_balance\s*[*+/\-]\s*[0-9.]+"
        message = re.sub(formula_pattern, compute_formula, self.message_template)
        # Replace plain ar_balance (not part of a formula)
        def replace_plain_ar_balance(m):
            try:
                value = round(float(ar_balance) + 1e-8, 2)
                return f"{value:.2f}"
            except Exception:
                return str(ar_balance)
        message = re.sub(r"ar_balance(?!\s*[*+/\-])", replace_plain_ar_balance, message)
        message = message.replace("account_no", account_no)
        if customer_name:
            message = message.replace("customer_name", customer_name)
        return message

    def send_sms(
        self,
        destination: str,
        api_key: str,
        api_secret: str,
        url: str,
        origin: str = "REMINDER",
    ) -> bool:
        ts = int(time.time())
        nonce = secrets.token_urlsafe(7)
        mac_string = self._build_mac_string(ts, nonce)
        mac_signature = self._calculate_mac(mac_string, api_secret)

        headers = self._build_headers(api_key, ts, nonce, mac_signature)
        payload = self._build_payload(destination, origin)

        response = requests.post(url, headers=headers, json=payload, verify=False)
        return self._is_successful(response)

    def _build_mac_string(self, ts: int, nonce: str) -> str:
        return f"{ts}\n{nonce}\nPOST\n/v2/sms/\napi.smsglobal.com\n443\n\n"

    def _build_headers(self, api_key: str, ts: int, nonce: str, mac: str) -> dict[str, str]:
        return {
            "Authorization": f'MAC id="{api_key}", ts="{ts}", nonce="{nonce}", mac="{mac}"',
            "Content-Type": "application/json",
        }

    def _build_payload(self, destination: str, origin: str) -> dict[str, str]:
        return {
            "origin": origin,
            "destination": str(destination),
            "message": self.message_template,
        }

    def _is_successful(self, response: requests.Response) -> bool:
        if response.status_code == 200:
            try:
                data = response.json()
                messages = data.get("messages", [])
                if messages:
                    status = messages[0].get("status", "").lower()
                    return status in {"sent", "delivered", "queued"}
            except (ValueError, KeyError):
                pass
        return False

    @staticmethod
    def _calculate_mac(data: str, secret: str) -> str:
        digest = hmac.new(secret.encode(), data.encode(), hashlib.sha256).digest()
        return base64.b64encode(digest).decode()

def main() -> None:
    template = "Dear customer_name, your account account_no has a balance of ar_balance."
    sender = SMSSender(template)
    # Example with formula: ar_balance * 1.015
    template_formula = "Dear customer_name, your account account_no has a balance of ar_balance*1.015."
    sender_formula = SMSSender(template_formula)
    message = sender_formula.replace_keywords("123456", "100.00", "John Doe")
    print("Generated message with formula:", message)
    # Example with formula: ar_balance + 5
    template_plus = "Dear customer_name, your account account_no has a balance of ar_balance+5."
    sender_plus = SMSSender(template_plus)
    message2 = sender_plus.replace_keywords("123456", "100.00", "John Doe")
    print("Generated message with +5:", message2)

if __name__ == "__main__":
    main()
