from uuid import uuid4
import pytest
from json import dumps
import requests


@pytest.fixture(scope="class", autouse=False)
def create_todo():
    url_todo = "https://apichallenges.herokuapp.com/todos"
    todo_title = f"title {str(uuid4())}"
    payload = dumps(
        {
            "title": todo_title,
            "doneStatus": True,
            "description": "qua. Ut enim ad mini",
        }
    )
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    response = requests.post(url=url_todo, data=payload, headers=headers)

    assert (
        response.status_code == 201
    ), f"Request error, wrong status code - {response.status_code}"

    todo_list = requests.get(url_todo)
    modified_list = todo_list.json()["todos"]
    new_todo = [todo for todo in modified_list if todo["title"] == todo_title][0]
    todo_id = new_todo["id"]
    assert len(new_todo) != 0, f"New todo not added into the list"

    yield todo_id
