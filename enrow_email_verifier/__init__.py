"""Verify email addresses for deliverability, catch-all detection, and more. Powered by Enrow."""

from typing import Any, Dict, List, Optional

import httpx

__all__ = ["verify_email", "get_verification_result", "verify_emails", "get_verification_results"]

BASE_URL = "https://api.enrow.io"


def _request(api_key: str, method: str, path: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers = {"x-api-key": api_key, "Content-Type": "application/json"}
    url = f"{BASE_URL}{path}"

    with httpx.Client() as client:
        response = client.request(method, url, headers=headers, json=body)

    data = response.json()
    if not response.is_success:
        raise Exception(data.get("message", f"API error {response.status_code}"))
    return data


def verify_email(
    api_key: str,
    email: str,
    webhook: Optional[str] = None,
) -> Dict[str, Any]:
    """Start a single email verification. Returns a dict with an 'id' to poll for results."""
    body: Dict[str, Any] = {"email": email}
    if webhook:
        body["settings"] = {"webhook": webhook}
    return _request(api_key, "POST", "/email/verify/single", body)


def get_verification_result(api_key: str, id: str) -> Dict[str, Any]:
    """Retrieve the result of a single email verification by its ID."""
    return _request(api_key, "GET", f"/email/verify/single?id={id}")


def verify_emails(
    api_key: str,
    emails: List[str],
    webhook: Optional[str] = None,
) -> Dict[str, Any]:
    """Start a bulk email verification. Returns a dict with a 'batchId' to poll for results."""
    body: Dict[str, Any] = {
        "verifications": [{"email": email} for email in emails],
    }
    if webhook:
        body["settings"] = {"webhook": webhook}
    return _request(api_key, "POST", "/email/verify/bulk", body)


def get_verification_results(api_key: str, id: str) -> Dict[str, Any]:
    """Retrieve the results of a bulk email verification by its batch ID."""
    return _request(api_key, "GET", f"/email/verify/bulk?id={id}")
