
import pytest
from pydantic import BaseModel
from googleapiclient.errors import HttpError
from your_component_path import (
    GoogleSheetUpdater,
    GoogleSheetUpdaterInputDict,
    GoogleSheetUpdaterOutputDict,
)

# Define test cases with mocked input and expected output data
test_cases = [
    (
        {"jailbreakRaterData": {"jailbreak1": 5, "jailbreak2": 3, "jailbreak3": 1}},
        {"updatedSheetId": "test_google_sheet_id"},
    ),
    (
        {"jailbreakRaterData": {}},
        {"updatedSheetId": "test_google_sheet_id"},
    ),
    (
        {"jailbreakRaterData": {"jailbreak1": -1}},
        {"updatedSheetId": "test_google_sheet_id"},
    ),
]

# Use @pytest.mark.parametrize to create multiple test scenarios
@pytest.mark.parametrize("input_data, expected_output", test_cases)
def test_transform(mocker, input_data, expected_output):
    # Mock the service_account.Credentials.from_service_account_file method
    mocker.patch(
        "component_path.service_account.Credentials.from_service_account_file",
        return_value="mocked_credentials",
    )

    # Mock the googleapiclient.discovery.build method
    mock_build = mocker.patch("component_path.build")

    # Mock the sheets_instance.spreadsheets().get(spreadsheetId).execute() method
    mock_spreadsheets_get_execute = mocker.patch.object(
        mock_build.return_value.spreadsheets.return_value,
        "get",
        return_value=mocker.MagicMock(execute=lambda: {"sheetId": "test_google_sheet_id"}),
    )

    # Mock the sheets_instance.spreadsheets().values().clear().execute() method
    mock_spreadsheets_values_clear_execute = mocker.patch.object(
        mock_build.return_value.spreadsheets.return_value.values.return_value,
        "clear",
        return_value=mocker.MagicMock(execute=lambda: None),
    )

    # Mock the sheets_instance.spreadsheets().values().append().execute() method
    mock_spreadsheets_values_append_execute = mocker.patch.object(
        mock_build.return_value.spreadsheets.return_value.values.return_value,
        "append",
        return_value=mocker.MagicMock(execute=lambda: None),
    )

    # Instantiate the component
    google_sheet_updater = GoogleSheetUpdater()

    # Modify googleSheetId to match the expected_output
    google_sheet_updater.googleSheetId = "test_google_sheet_id"

    # Call the component's transform() method with mocked input data
    output_data = google_sheet_updater.transform(GoogleSheetUpdaterInputDict(**input_data))

    # Assert that the output matches the expected output
    assert output_data == GoogleSheetUpdaterOutputDict(**expected_output)

    # Check if the methods were called with the correct arguments
    mock_spreadsheets_get_execute.assert_called_with(spreadsheetId="test_google_sheet_id")
    mock_spreadsheets_values_clear_execute.assert_called_with(
        spreadsheetId="test_google_sheet_id", range="A1:Z", body={}
    )

# Error handling test case
def test_transform_with_http_error(mocker):
    # Mock the service_account.Credentials.from_service_account_file method
    mocker.patch(
        "component_path.service_account.Credentials.from_service_account_file",
        return_value="mocked_credentials",
    )

    # Mock the googleapiclient.discovery.build method and raise an HttpError
    mocker.patch(
        "component_path.build",
        side_effect=HttpError(resp={"status": "400"}, content=b"Mocked HttpError content"),
    )

    # Instantiate the component
    google_sheet_updater = GoogleSheetUpdater()

    # Call the component's transform() method with mocked input data and handle the exception
    with pytest.raises(HttpError):
        google_sheet_updater.transform(
            GoogleSheetUpdaterInputDict(jailbreakRaterData={"jailbreak1": 5})
        )

