from dataclasses import dataclass
import requests

from src.config import Settings
from src.schema import GoogleUserData

@dataclass
class GoogleClient:
    settings: Settings

    def get_user_info(self, code: str) -> GoogleUserData:
        access_token = self._get_user_access_token(code=code)
        user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo",
                                 headers={"Authorizayion": f"Bearer {access_token}"})
        return GoogleUserData(**user_info.json())

    def _get_user_access_token(self, code: str) -> str:
        data ={
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        
        response = requests.get(self.settings.GOOGLE_TOKEN_URL, data=data)
        return response.json()['access_token'] 
