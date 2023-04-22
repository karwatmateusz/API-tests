from uuid import uuid4
import requests
import pytest
from json import dumps, loads
from pprint import pprint


class TestApi:
    _url_todo = "https://apichallenges.herokuapp.com/todos"
    _todo_title = f"title {str(uuid4())}"

    @pytest.mark.api
    def test_pay_invoices_in_todo_list(self):
        response = requests.get(self._url_todo)
        response_text = response.json()["todos"]
        assert (
            response.status_code == 200
        ), f"Request error, wrong status code - {response.status_code}"
        todo_title = [todo["title"] for todo in response_text]
        assert len(todo_title) != 0, f"List is empty"

    @pytest.mark.api
    def test_new_todo_can_be_added(self):
        payload = dumps(
            {
                "title": self._todo_title,
                "doneStatus": True,
                "description": "qua. Ut enim ad mini",
            }
        )
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response = requests.post(url=self._url_todo, data=payload, headers=headers)

        assert (
            response.status_code == 201
        ), f"Request error, wrong status code - {response.status_code}"

        todo_list = requests.get(self._url_todo)
        modified_list = todo_list.json()["todos"]
        new_todo = [todo for todo in modified_list if todo["title"] == self._todo_title]
        pprint(f"new todo is {new_todo}")
        assert len(new_todo) != 0, f"New todo not added into the list"

    @pytest.mark.dependency(depends=["create_todo"])
    @pytest.mark.api
    def test_specific_todo_can_be_retrieved(self, create_todo):
        todo_id = create_todo
        response = requests.get(f"{self._url_todo}/{todo_id}")
        response_text = response.json()
        assert (
            response.status_code == 200
        ), f"Request error, wrong status code - {response.status_code}"
        pprint(f"retrievew todo {response_text}")
        assert len(response_text) == 1, f"List is empty"

    @pytest.mark.dependency(depends=["create_todo"])
    @pytest.mark.api
    def test_specific_todo_can_be_updated(self, create_todo):
        todo_id = create_todo
        payload = dumps(
            {
                "title": "new updated title",
            }
        )
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        url_to_specific_todo = f"{self._url_todo}/{todo_id}"
        response = requests.post(
            url=url_to_specific_todo, data=payload, headers=headers
        )
        assert (
            response.status_code == 200
        ), f"Request failed, todo not updated - status code {response.status_code}"

        updated_response = requests.get(url_to_specific_todo)
        updated_todo = updated_response.json()
        print(f"updated todo is {updated_todo}")

    @pytest.mark.api
    def test_specific_todo_can_be_deleted(self):
        pass
