from uuid import uuid4
import pytest
from json import dumps
import requests


@pytest.fixture(scope="class", autouse=False)
def create_todo():
    url_todo = "https://apichallenges.herokuapp.com/todos"
    todo_title = f"title"
    payload = dumps(
        {
            "title": todo_title,
            "doneStatus": True,
            "description": "qua. Ut enim ad mini",
        }
    )
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    response = requests.post(url=url_todo, data=payload, headers=headers)
    if response.status_code == 204:
        todo_list = requests.get(url_todo)
        modified_list = todo_list.json()["todos"]
        new_todo = [todo for todo in modified_list if todo["title"] == todo_title][0]
        todo_id = new_todo["id"]
        yield todo_id
