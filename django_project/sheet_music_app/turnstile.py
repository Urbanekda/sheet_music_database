"""Server-side verification for Cloudflare Turnstile tokens.

See: https://developers.cloudflare.com/turnstile/get-started/server-side-validation/
"""
import requests
from django.conf import settings

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


def verify_turnstile_token(token, remote_ip=None):
    """Return True if the given Turnstile response token is valid."""
    if not token or not settings.TURNSTILE_SECRET_KEY:
        return False

    payload = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token,
    }
    if remote_ip:
        payload["remoteip"] = remote_ip

    try:
        response = requests.post(TURNSTILE_VERIFY_URL, data=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return False

    return response.json().get("success", False)
