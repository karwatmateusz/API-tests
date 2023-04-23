import pytest

@pytest.fixture
def valid_user_credentials():
    user_mail = "tracey.ramos@reqres.in"
    user_password = "some_password"
    return user_mail, user_password

@pytest.fixture
def valid_user_payload(valid_user_credentials):
    email, password = valid_user_credentials
    return {"email": email, "password": password}

@pytest.fixture
def invalid_user_credentials():
    user_mail = "@mail.com"
    user_password = "testpass"
    return user_mail, user_password

@pytest.fixture
def invalid_user_payload(invalid_user_credentials):
    email, password = invalid_user_credentials
    return {"email": email, "password": password}