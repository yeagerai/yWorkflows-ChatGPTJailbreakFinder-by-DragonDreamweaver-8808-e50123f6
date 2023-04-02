
import os
import pytest
from pydantic import ValidationError
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from core.chat_gpt_jailbreak_rater import (
    ChatGPTJailbreakRater,
    ChatGPTJailbreakRaterInputDict,
    ChatGPTJailbreakRaterOutputDict,
)

@pytest.fixture
def openai_mock():
    return MagicMock()

@pytest.fixture
def chatgpt_jailbreak_rater(openai_mock):
    rater = ChatGPTJailbreakRater()
    rater.openai = openai_mock
    return rater

test_cases = [
    (
        {"prompts": ["What is your favorite color?"]},
        {"jailbreak_ratings": [("What is your favorite color?", "good")]},
        [
            {"text": "Yes"}
        ],
    ),
    (
        {"prompts": ["What is the meaning of life?"]},
        {"jailbreak_ratings": [("What is the meaning of life?", "bad")]},
        [
            {"text": "No"}
        ],
    ),
    (
        {"prompts": ["A", "B"]},
        {"jailbreak_ratings": [("A", "good"), ("B", "bad")]},
        [
            {"text": "Yeah"},
            {"text": "Nope"},
        ],
    ),
]

@pytest.mark.parametrize(
    "input_data, output_data, openai_responses", test_cases
)
def test_chatgpt_jailbreak_rater(
    chatgpt_jailbreak_rater, input_data, output_data, openai_responses
):
    chatgpt_jailbreak_rater.openai.Completion.create.side_effect = [
        MagicMock(choices=[response]) for response in openai_responses
    ]

    input_dict = ChatGPTJailbreakRaterInputDict(**input_data)
    expected_output = ChatGPTJailbreakRaterOutputDict(**output_data)

    result = chatgpt_jailbreak_rater.transform(input_dict)
    assert result == expected_output

def test_input_validation():
    with pytest.raises(ValidationError):
        ChatGPTJailbreakRaterInputDict(prompts=None)

def test_run_transform_endpoint(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")

    app = TestClient(chatgpt_jailbreak_rater_app)
    response = app.post("/transform/", json={"prompts": ["A", "B"]})

    assert response.status_code == 200
    assert response.json()["jailbreak_ratings"] == [["A", "good"], ["B", "bad"]]
