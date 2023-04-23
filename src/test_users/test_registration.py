import pytest
import requests
from json import dumps
import jsonschema


class TestUserRegistration:
    registration_successfull_schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "token": {"type": "string"},
        },
        "required": ["id", "token"],
    }

    registration_failed_schema = {
        "type": "object",
        "properties": {"error": {"type": "string"}},
        "required": ["error"],
    }

    def setup_method(self):
        self.base_api_url = "https://reqres.in/api"
        self.registration_endpoint = f"{self.base_api_url}/register"
        self.user_mail = "tracey.ramos@reqres.in"
        self.user_password = "some_password"
        self.header = {"Content-Type": "application/json"}

    @pytest.mark.registration
    def test_registration_return_token(self):
        payload = dumps({"email": self.user_mail, "password": self.user_password})
        response = requests.post(
            url=self.registration_endpoint, data=payload, headers=self.header
        )
        assert response.status_code == 200
        assert "token" in response.json()

    @pytest.mark.registration
    def test_user_cant_register_without_password(self):
        payload = dumps({"email": self.user_mail})
        response = requests.post(
            url=self.registration_endpoint, data=payload, headers=self.header
        )
        assert response.status_code == 400
        error_message = response.json()["error"]
        assert "Missing password" in error_message

    @pytest.mark.registration
    def test_user_cant_register_without_email(self):
        payload = dumps({"password": self.user_password})
        response = requests.post(
            url=self.registration_endpoint, data=payload, headers=self.header
        )
        assert response.status_code == 400
        error_message = response.json()["error"]
        assert "Missing email or username" in error_message

    @pytest.mark.registration
    def test_register_not_defined_user(self):
        payload = dumps({"email": "some_user", "password": "anypassword"})
        response = requests.post(
            url=self.registration_endpoint, data=payload, headers=self.header
        )
        assert response.status_code == 400
        error_message = response.json()["error"]
        assert "Only defined users succeed registration" in error_message

    @pytest.mark.login_schema
    def test_user_registration_successfull_has_expected_schema(
        self, valid_user_payload
    ):
        response = requests.post(
            url=self.registration_endpoint, headers=self.header, json=valid_user_payload
        )
        jsonschema.validate(
            instance=response.json(), schema=self.registration_successfull_schema
        )

    @pytest.mark.login_schema
    def test_user_registration_failed_has_expected_schema(self, invalid_user_payload):
        response = requests.post(
            url=self.registration_endpoint,
            headers=self.header,
            json=invalid_user_payload,
        )
        jsonschema.validate(
            instance=response.json(), schema=self.registration_failed_schema
        )
