
import pytest
import requests
from bs4 import BeautifulSoup
from unittest import mock
from pydantic import ValidationError

from core.abstract_component import AbstractComponent
from name_of_your_file import (JailbreakScraper,
                               JailbreakScraperInputDict,
                               JailbreakScraperOutputDict)

# Define test cases with mocked input and expected output data
test_data = [
    {
        "input": JailbreakScraperInputDict(),
        "output": JailbreakScraperOutputDict(
            top_10_prompts=[
                {"prompt": "Example Prompt 1", "jbscore": 5.0},
                {"prompt": "Example Prompt 2", "jbscore": 4.5},
                {"prompt": "Example Prompt 3", "jbscore": 4.0},
                # Add more prompts to reach a total of 10
            ]
        )
    },
    {
        "input": JailbreakScraperInputDict(),
        "output": JailbreakScraperOutputDict(
            top_10_prompts=[
                # Add different sorted prompts here if needed
            ]
        )
    },
    # Add more test scenarios if needed
]

# Mock the requests.get() and BeautifulSoup() calls
def mocked_requests_get(*args, **kwargs):
    # Define the response object to return instead of actual API call
    class MockResponse:
        def __init__(self, content):
            self.content = content

    response_content = b"""
    <html>
    <body>
        <div class="prompt">
            <h3>Example Prompt 1</h3>
            <span class="jbscore">5.0</span>
        </div>
        <div class="prompt">
            <h3>Example Prompt 2</h3>
            <span class="jbscore">4.5</span>
        </div>
        <div class="prompt">
            <h3>Example Prompt 3</h3>
            <span class="jbscore">4.0</span>
        </div>
        <!-- Add more mocked prompts here if needed -->
    </body>
    </html>
    """

    return MockResponse(response_content)


def mocked_beautiful_soup(*args, **kwargs):
    return BeautifulSoup(args[0], "html.parser")


# Use @pytest.mark.parametrize to create multiple test scenarios
@pytest.mark.parametrize("data", test_data)
def test_jailbreak_scraper_transform(data):
    jailbreak_scraper = JailbreakScraper()

    # Patch the requests.get and BeautifulSoup calls
    with mock.patch("requests.get", side_effect=mocked_requests_get):
        with mock.patch("bs4.BeautifulSoup", side_effect=mocked_beautiful_soup):
            result = jailbreak_scraper.transform(data["input"])

    # Assert that the output matches the expected output
    assert result == data["output"]


# Error handling and edge case scenarios
def test_jailbreak_scraper_invalid_input():
    # Test with an input value that's not an instance of JailbreakScraperInputDict
    with pytest.raises(ValidationError):
        invalid_input = "Invalid Input"
        jailbreak_scraper = JailbreakScraper()
        result = jailbreak_scraper.transform(invalid_input)
