import pytest
import requests


class TestVCR:
    @pytest.mark.vcr
    def test_user_not_logged_with_invalid_credentials(self):
        payload = {"email": "some_mail@reqres.in", "password": "some_password"}
        with requests.post("https://reqres.in/api/login", json=payload) as response:
            assert response.status_code == 400
            error_message = response.json()["error"]
            assert "user not found" in error_message
