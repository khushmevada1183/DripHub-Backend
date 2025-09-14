import os
from typing import Optional
import httpx
from app.core.config import settings


class SupabaseClient:
    def __init__(self, url: Optional[str] = None, anon_key: Optional[str] = None, service_role: Optional[str] = None):
        self.url = url or settings.SUPABASE_URL
        self.anon_key = anon_key or settings.SUPABASE_ANON_KEY
        self.service_role = service_role or settings.SUPABASE_SERVICE_ROLE_KEY

    async def get_user(self, jwt_token: str) -> dict:
        """Return the user object for a Supabase JWT token or raise an httpx.HTTPError on transport issues.

        This uses the Supabase auth endpoint: /auth/v1/user
        """
        if not self.url:
            raise RuntimeError("Supabase URL not configured")
        apikey = self.anon_key or self.service_role
        if not apikey:
            raise RuntimeError("Supabase API key not configured")

        headers = {"Authorization": f"Bearer {jwt_token}", "apikey": apikey}
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{self.url}/auth/v1/user", headers=headers, timeout=10.0)
        if r.status_code != 200:
            raise httpx.HTTPStatusError("Invalid token", request=r.request, response=r)
        return r.json()

    async def signup(self, email: str, password: str) -> dict:
        """Sign up a user in Supabase and return the response JSON (may include an access token/session).

        Docs: POST /auth/v1/signup
        """
        if not self.url:
            raise RuntimeError("Supabase URL not configured")
        apikey = self.anon_key or self.service_role
        if not apikey:
            raise RuntimeError("Supabase API key not configured")

        headers = {"apikey": apikey, "Content-Type": "application/json"}
        payload = {"email": email, "password": password}
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{self.url}/auth/v1/signup", json=payload, headers=headers, timeout=10.0)
        # Return raw JSON so caller can decide how to handle (session, user, etc.).
        return {"status_code": r.status_code, "json": r.json()}

    async def sign_in(self, email: str, password: str) -> dict:
        """Sign in a user via Supabase and return the token/session JSON.

        Docs: POST /auth/v1/token?grant_type=password
        """
        if not self.url:
            raise RuntimeError("Supabase URL not configured")
        apikey = self.anon_key or self.service_role
        if not apikey:
            raise RuntimeError("Supabase API key not configured")

        headers = {"apikey": apikey, "Content-Type": "application/json"}
        payload = {"email": email, "password": password}
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{self.url}/auth/v1/token?grant_type=password", json=payload, headers=headers, timeout=10.0)
        return {"status_code": r.status_code, "json": r.json()}

    async def admin_create_user(self, email: str, password: str, email_confirm: bool = False) -> dict:
        """Create a user via the Supabase Admin API using the service_role key.

        When `email_confirm` is True, the created user will be marked as confirmed
        and will not require email verification.
        """
        if not self.url:
            raise RuntimeError("Supabase URL not configured")
        if not self.service_role:
            raise RuntimeError("Supabase service role key not configured")

        headers = {"apikey": self.service_role, "Authorization": f"Bearer {self.service_role}", "Content-Type": "application/json"}
        payload = {"email": email, "password": password}
        if email_confirm:
            payload["email_confirm"] = True

        async with httpx.AsyncClient() as client:
            r = await client.post(f"{self.url}/auth/v1/admin/users", json=payload, headers=headers, timeout=10.0)
        return {"status_code": r.status_code, "json": r.json()}

    async def health_check(self) -> dict:
        """Basic health check for the Supabase URL. Returns a dict with status info.

        This is best-effort: we try a GET on /health and fall back to root.
        Any transport error will raise httpx.HTTPError to the caller.
        """
        if not self.url:
            raise RuntimeError("Supabase URL not configured")
        apikey = self.anon_key or self.service_role
        headers = {"apikey": apikey} if apikey else {}
        async with httpx.AsyncClient() as client:
            # Try a known health endpoint, otherwise fall back to root
            for path in ("/health", "/", ""):
                try:
                    r = await client.get(f"{self.url.rstrip('/')}{path}", headers=headers, timeout=5.0)
                except httpx.RequestError:
                    # Try next
                    continue
                return {"status_code": r.status_code, "ok": r.status_code == 200, "path": path}
        raise httpx.RequestError("Could not reach Supabase URL")


supabase_client = SupabaseClient()
