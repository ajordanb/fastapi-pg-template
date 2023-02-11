import requests 
from .config import settings

class Proxy():
    def __init__(self) -> None:
        self.username = settings.proxy_username
        self.password = settings.proxy_password
        self.url = settings.proxy_url 
        self._token = None
    def token(self):
        if self._token:
            return self._token
        url = f"{self.url}login"
        data = {"username": self.username, "password": self.password}
        headers = {}
        headers["accept"] = "application/json"
        headers = {
            "accept": "application/json",
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            self._token = response.json()["access_token"]
            return response.json()["access_token"]
        else:
            raise Exception(response.status_code)
        
    def send_email(self,email_text:str, subject:str, recipient_name:str, recipient_email:str):
        params = {
            'subject': subject,
            'email_text': email_text,
            'recipient_name': recipient_name,
        }
        json_data = {
    'email': recipient_email,
}
        return self.post_request(
            'email/send_plain_email',
            json_data,
            params
        )
    
    def post_request(self, endpoint, data, params):
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.token()}",
        }
        if params != '':
             response = requests.post(f"{self.url}{endpoint}",params=params, headers=headers, json=data)
        else:
            response = requests.post(f"{self.url}{endpoint}", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(response.status_code)
        
