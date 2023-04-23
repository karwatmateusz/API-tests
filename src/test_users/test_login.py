import pytest
import requests
from json import dumps


class TestUserLogin:
    def setup_method(self):
        self.base_api_url = "https://reqres.in/api"
        self.login_endpoint = f"{self.base_api_url}/login"
        self.user_mail = "tracey.ramos@reqres.in"
        self.user_password = "some_password"
        self.header = {"Content-Type": "application/json"}

    @pytest.mark.login
    def test_user_can_login_with_valid_credentials(self):
        payload = dumps({"email": self.user_mail, "password": self.user_password})
        response = requests.post(
            url=self.login_endpoint, headers=self.header, data=payload
        )
        assert response.status_code == 200
        assert "token" in response.json()

    @pytest.mark.login
    def test_user_not_logged_with_invalid_credentials(self):
        payload = dumps({"email": "invalid@email.com", "password": "somepassword"})
        response = requests.post(
            url=self.login_endpoint, headers=self.header, data=payload
        )
        assert response.status_code == 400
        error_message = response.json()["error"]
        assert "user not found" in error_message

    @pytest.mark.login
    def test_user_not_logged_without_email(self):
        payload = dumps({"password": self.user_password})
        response = requests.post(
            url=self.login_endpoint, headers=self.header, data=payload
        )
        assert response.status_code == 400
        error_message = response.json()["error"]
        assert "Missing email or username" in error_message

    @pytest.mark.login
    def test_user_not_logged_without_password(self):
        payload = dumps({"email": self.user_mail})
        response = requests.post(
            url=self.login_endpoint, headers=self.header, data=payload
        )
        assert response.status_code == 400
        error_message = response.json()["error"]
        assert "Missing password" in error_message
