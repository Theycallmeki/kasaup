from urllib.parse import urlencode
import httpx
from app.core.config import settings

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
USER_URL = "https://api.github.com/user"
EMAILS_URL = "https://api.github.com/user/emails"


def get_github_auth_url(role: str = "customer"):
    params = {
        "client_id": settings.GH_CLIENT_ID,
        "redirect_uri": settings.GH_REDIRECT_URI,
        "scope": "read:user user:email",
        "state": role
    }
    return f"{GITHUB_AUTH_URL}?{urlencode(params)}"


async def get_github_user(code: str):
    async with httpx.AsyncClient() as client:
        # 1. Get access token
        token_res = await client.post(
            TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.GH_CLIENT_ID,
                "client_secret": settings.GH_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.GH_REDIRECT_URI
            }
        )
        
        if token_res.status_code != 200:
            raise Exception(f"Failed to get github token: {token_res.text}")
            
        token_data = token_res.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise Exception(f"GitHub access token missing in response: {token_data}")
            
        headers = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "Kasaup-App"
        }
        
        # 2. Get user profile
        user_res = await client.get(USER_URL, headers=headers)
        if user_res.status_code != 200:
            raise Exception(f"Failed to get user info from github: {user_res.text}")
            
        user_data = user_res.json()
        email = user_data.get("email")
        
        # 3. If email is private, get it from /user/emails
        if not email:
            emails_res = await client.get(EMAILS_URL, headers=headers)
            if emails_res.status_code == 200:
                emails = emails_res.json()
                for e in emails:
                    if e.get("primary") and e.get("verified"):
                        email = e.get("email")
                        break
                        
        if not email:
            raise Exception("GitHub account must have a primary verified email.")
            
        return {
            "email": email,
            "name": user_data.get("name") or user_data.get("login"),
            "picture": user_data.get("avatar_url")
        }
