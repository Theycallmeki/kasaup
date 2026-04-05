from urllib.parse import urlencode
import httpx
from app.core.config import settings

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def get_google_auth_url(role: str = "customer"):
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
        "state": role
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"


async def get_google_user(code: str):
    async with httpx.AsyncClient() as client:
        token_res = await client.post(TOKEN_URL, data={
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code"
        })

        if token_res.status_code != 200:
            raise Exception(f"Failed to get google token: {token_res.text}")

        token_data = token_res.json()

        user_res = await client.get(
            USERINFO_URL,
            headers={"Authorization": f"Bearer {token_data['access_token']}"}
        )

        if user_res.status_code != 200:
            raise Exception(f"Failed to get user info from google: {user_res.text}")

        return user_res.json()
