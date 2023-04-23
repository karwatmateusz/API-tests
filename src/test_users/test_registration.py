import pytest
import requests
from json import dumps


class TestUserRegistration:
    def setup_method(self):
        self.base_api_url = "https://reqres.in/api"
        self.registration_endpoint = f"{self.base_api_url}/register"
        self.user_mail = "tracey.ramos@reqres.in"
        self.user_password = "some_password"
        self.header = {"Content-Type": "application/json"}

    def test_registration_return_token(self):
        payload = dumps({"email": self.user_mail, "password": self.user_password})
        response = requests.post(
            url=self.registration_endpoint, data=payload, headers=self.header
        )
        assert response.status_code == 200
        assert "token" in response.json()

    def test_user_cant_register_without_password(self):
        payload = dumps({"email": self.user_mail})
        response = requests.post(
            url=self.registration_endpoint, data=payload, headers=self.header
        )
        assert response.status_code == 400
        error_message = response.json()["error"]
        assert "Missing password" in error_message

    def test_user_cant_register_without_email(self):
        payload = dumps({"password": self.user_password})
        response = requests.post(
            url=self.registration_endpoint, data=payload, headers=self.header
        )
        assert response.status_code == 400
        error_message = response.json()["error"]
        assert "Missing email or username" in error_message

    def test_register_not_defined_user(self):
        payload = dumps({"email": "some_user", "password": "anypassword"})
        response = requests.post(
            url=self.registration_endpoint, data=payload, headers=self.header
        )
        assert response.status_code == 400
        error_message = response.json()["error"]
        assert "Only defined users succeed registration" in error_message
