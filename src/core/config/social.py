from pydantic_settings import BaseSettings


class SocialAuthConfig(BaseSettings):
    GOOGLE_CLIENT_ID: str | None = None
    GOOGLE_CLIENT_SECRET: str | None = None
    GOOGLE_REDIRECT_URI: str = (
        "http://localhost:8000/api/v1/social_auth/google/callback"
    )

    @property
    def OAUTH_PROVIDERS(self):
        return {
            "google": {
                "client_id": self.GOOGLE_CLIENT_ID,
                "client_secret": self.GOOGLE_CLIENT_SECRET,
                "authorize_url": "https://accounts.google.com/o/oauth2/v2/auth",
                "token_url": "https://oauth2.googleapis.com/token",
                "userinfo_url": "https://openidconnect.googleapis.com/v1/userinfo",
                "redirect_uri": self.GOOGLE_REDIRECT_URI,
            }
        }
