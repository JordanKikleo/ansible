import requests


class Thingsboard:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.host = "https://thingsboard.kikleo.com:443/api"
        self.headers = {"X-Authorization": f"Bearer { self.auth_login() }"}

    def auth_login(self):
        """Se connecter à Thingsboard et recevoir un token"""
        tb_credentials = {"username": self.username, "password": self.password}
        url = f"{self.host}/auth/login"
        return (requests.post(url, json=tb_credentials).json())["token"]

    def create_device(self, data):
        url = f"{self.host}/device"
        return requests.post(url, headers=self.headers, json=data)

    def get_all_devices(self, customer_id, page_size=1000):
        """
        Récupérer tous les devices créés dans Thingsboard
        """
        url = f"{self.host}/customer/{customer_id}/devices?pageSize={page_size}&page=0"
        return (requests.get(url, headers=self.headers).json())["data"]

    def get_device_credentials(self, device_id):
        url = f"{self.host}/device/{device_id}/credentials"
        return (requests.get(url, headers=self.headers).json())["credentialsId"]

    def create_device_attributes(self, device_id, data, scope):
        """
        Créer un shared attribute
        SERVER_SCOPE | SHARED_SCOPE
        """
        url = f"{self.host}/plugins/telemetry/DEVICE/{device_id}/attributes/{scope}"
        return requests.post(url, headers=self.headers, json=data)
