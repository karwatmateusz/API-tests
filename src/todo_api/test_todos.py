from uuid import uuid4
import requests
import pytest
from json import dumps, loads
from pprint import pprint


class TestApi:
    _url_todo = "https://apichallenges.herokuapp.com/todos"
    _todo_title = f"title {str(uuid4())}"

    @pytest.mark.api
    def test_todo_list_is_not_empty(self):
        response = requests.get(self._url_todo)
        response_text = response.json()["todos"]
        assert (
            response.status_code == 200
        ), f"Request error, wrong status code - {response.status_code}"
        todo_list = [todo for todo in response_text]
        assert (
            len(todo_list) != 0
        ), f"Expected to find at least one todo item in the list ({len(todo_list)} found)"

    @pytest.mark.api
    def test_todo_can_be_created(self):
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
    def test_todo_can_be_retrieved_by_id(self, create_todo):
        todo_id = create_todo
        response = requests.get(f"{self._url_todo}/{todo_id}")
        response_text = response.json()
        assert (
            response.status_code == 200
        ), f"Request error, wrong status code - {response.status_code}"
        pprint(f"retrievew todo {response_text}")
        assert (
            len(response_text) == 1
        ), f"Expected to retrieve one todo item (id={todo_id}), but found {len(response_text)} items"

    @pytest.mark.dependency(depends=["create_todo"])
    @pytest.mark.api
    def test_todo_can_be_updated_by_id(self, create_todo):
        todo_id = create_todo
        payload = dumps(
            {
                "title": "new updated title",
            }
        )
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        specific_todo_url = f"{self._url_todo}/{todo_id}"
        response = requests.post(url=specific_todo_url, data=payload, headers=headers)
        assert (
            response.status_code == 200
        ), f"Failed to update todo item (id={todo_id}, title='new updated title'), status code {response.status_code}"

        updated_response = requests.get(specific_todo_url)
        updated_todo = updated_response.json()
        print(f"updated todo is {updated_todo}")

    @pytest.mark.api
    def test_todo_can_be_deleted_by_id(self, create_todo):
        todo_id = create_todo
        specific_todo_url = f"{self._url_todo}/{todo_id}"
        response = requests.delete(specific_todo_url)
        assert (
            response.status_code == 200
        ), f"Failed to delete todo item (id={todo_id}), status code {response.status_code}"

        specific_todo_item = requests.get(specific_todo_url)
        assert specific_todo_item.status_code == 404
