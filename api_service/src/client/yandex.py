from dataclasses import dataclass
import requests

from src.config import Settings
from src.schema import YandexUserData


@dataclass
class YandexClient:
    settings: Settings

    def get_user_info(self, code: str) -> YandexUserData:
        proxies = {
            'http': 'http://proxy.giop.local:3128',
            'https': 'http://proxy.giop.local:3128'
        }
        access_token = self._get_user_access_token(code=code)
        user_info = requests.get(
            'https://login.yandex.ru/info?format=json',
            headers={'Authorization': f'OAuth {access_token}'},
            proxies=proxies
        )
        return YandexUserData(**user_info.json(), access_token=access_token)
    
    def _get_user_access_token(self, code: str) -> str:
        proxies = {
            'http': 'http://proxy.giop.local:3128',
            'https': 'http://proxy.giop.local:3128'
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.settings.YANDEX_CLIENT_ID,
            "client_secret": self.settings.YANDEX_CLIENT_SECRET
        }

        response = requests.post(
            self.settings.YANDEX_TOKEN_URL,
            data=data,
            headers={'Content-type': 'application/x-www-form-urlencoded'},
            proxies=proxies
        )
        return response.json()['access_token']