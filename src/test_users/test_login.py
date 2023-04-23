import pytest
import requests
from json import dumps


class TestUserLogin:
    def setup_method(self):
        self.base_api_url = "https://reqres.in/api"
        self.login_endpoint = f"{self.base_api_url}/login"
        self.header = {"Content-Type": "application/json"}

    @pytest.fixture
    def valid_user_credentials(self):
        user_mail = "tracey.ramos@reqres.in"
        user_password = "some_password"
        return user_mail, user_password

    @pytest.fixture
    def valid_user_payload(self, valid_user_credentials):
        email, password = valid_user_credentials
        return {"email": email, "password": password}

    @pytest.fixture
    def invalid_user_credentials(self):
        user_mail = "@mail.com"
        user_password = "testpass"
        return user_mail, user_password

    @pytest.fixture
    def invalid_user_payload(self, invalid_user_credentials):
        email, password = invalid_user_credentials
        return {"email": email, "password": password}

    @pytest.mark.login
    def test_user_can_login_with_valid_credentials(self, valid_user_payload):
        with requests.post(
            url=self.login_endpoint, headers=self.header, json=valid_user_payload
        ) as response:
            assert response.status_code == 200
            assert "token" in response.json()

    @pytest.mark.login
    def test_user_not_logged_with_invalid_credentials(self, invalid_user_payload):
        with requests.post(
            self.login_endpoint, headers=self.header, json=invalid_user_payload
        ) as response:
            assert response.status_code == 400
            error_message = response.json()["error"]
            assert "user not found" in error_message

    @pytest.mark.login
    def test_user_not_logged_without_email(self, valid_user_payload):
        del valid_user_payload["email"]
        with requests.post(
            url=self.login_endpoint, headers=self.header, json=valid_user_payload
        ) as response:
            assert response.status_code == 400
            error_message = response.json()["error"]
            assert "Missing email or username" in error_message

    @pytest.mark.login
    def test_user_not_logged_without_password(self, valid_user_payload):
        del valid_user_payload["password"]
        with requests.post(
            url=self.login_endpoint, headers=self.header, json=valid_user_payload
        ) as response:
            assert response.status_code == 400
            error_message = response.json()["error"]
            assert "Missing password" in error_message
