import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer
from onedrivesdk import OneDriveClient


class OneDrive():
    def __init__(self, redirect_uri, client_secret, client_id, folder_id) -> None:
        self.api_base_url = 'api_base_url'
        self.scopes = ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']
        self.redirect_uri = redirect_uri
        self.client_secret = client_secret
        self.client_id = client_id
        self.folder_id = folder_id

    def authenticate_and_get_client(self):
        client = onedrivesdk.get_default_client(
            client_id=self.client_id, scopes=self.scopes)
        auth_url = client.auth_provider.get_auth_url(self.redirect_uri)
        code = GetAuthCodeServer.get_auth_code(auth_url, self.redirect_uri)
        client.auth_provider.authenticate(
            code, self.redirect_uri, self.client_secret)
        return client

    def list_directory_items(self):
        items = {}
        client = self.authenticate_and_get_client()
        folder = client.item(id="root").children.get()
        for item in folder:
            items[item.id] = item.name
        return items

    def download_item(self):
        client = self.authenticate_and_get_client()


client_id = '3e8a1902-85d0-4113-a4db-669b1168400b'
client_secret = 'yqw8Q~o2GHdLrfGCCRPFc2s3TcRHw4_OAgZPXbpN'
folder_id = 'EC64645612F3F1D3'
redirect = 'http://localhost:53682/'


od = OneDrive(redirect, client_secret, client_id, folder_id)

ls = od.list_directory_items()

print(ls)
