
import pytest
from pydantic import ValidationError
from typing import Any, Tuple
from your_module_path import ChatGPTJailbreakFinder, ChatGPTJailbreakFinderIn, ChatGPTJailbreakFinderOut

# Define test cases with mocked input and expected output data
TEST_CASES = [
    (
        ChatGPTJailbreakFinderIn(GoogleApiKey="fake_key_1"),
        ChatGPTJailbreakFinderOut(UpdatedGoogleSheetId="fake_sheet_id_1"),
    ),
    (
        ChatGPTJailbreakFinderIn(GoogleApiKey="fake_key_2"),
        ChatGPTJailbreakFinderOut(UpdatedGoogleSheetId="fake_sheet_id_2"),
    ),
]

# Error cases for testing invalid input
ERROR_CASES = [
    {"GoogleApiKey": "", "error_type": ValidationError},  # empty API key
]


@pytest.mark.parametrize(
    "mocked_input, expected_output",
    TEST_CASES,
    ids=["Test Case 1", "Test Case 2"],
)
async def test_transform(mocked_input: ChatGPTJailbreakFinderIn, expected_output: ChatGPTJailbreakFinderOut) -> None:
    # Instantiate the class
    chatgpt_jailbreak_finder = ChatGPTJailbreakFinder()

    # Call the transform() method
    output = await chatgpt_jailbreak_finder.transform(mocked_input, callbacks=None)

    # Assert that the output matches the expected output
    assert output == expected_output


@pytest.mark.parametrize("error_data, error_type", ERROR_CASES, ids=["Error Case 1"])
def test_transform_error_cases(
    error_data: dict, error_type: Any
) -> None:
    # Test if the transform method raises the expected error for given inputs
    with pytest.raises(error_type):
        ChatGPTJailbreakFinderIn(**error_data)
