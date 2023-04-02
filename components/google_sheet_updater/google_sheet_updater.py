
import os
import yaml
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from core.abstract_component import AbstractComponent


class GoogleSheetUpdaterInputDict(BaseModel):
    jailbreakRaterData: dict


class GoogleSheetUpdaterOutputDict(BaseModel):
    updatedSheetId: str


class GoogleSheetUpdater(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()
        with open(self.component_configuration_path(), "r", encoding="utf-8") as file:
            yaml_data = yaml.safe_load(file)

        self.googleSheetId = yaml_data["parameters"]["googleSheetId"]
        self.updateFrequency = yaml_data["parameters"]["updateFrequency"]

    def transform(
        self, args: GoogleSheetUpdaterInputDict
    ) -> GoogleSheetUpdaterOutputDict:
        jailbreakRaterData = args.jailbreakRaterData

        # Sorting the jailbreaks by their respective ratings
        sorted_jailbreaks = sorted(
            jailbreakRaterData.items(), key=lambda x: x[1], reverse=True
        )

        # Access the Google Sheet with the provided googleSheetId
        credentials = service_account.Credentials.from_service_account_file(
            "path/to/your/service-account-key.json"
        )
        sheets_instance = build("sheets", "v4", credentials=credentials)
        sheet = sheets_instance.spreadsheets().get(spreadsheetId=self.googleSheetId).execute()

        # Clear the Google Sheet and add new header with the appropriate columns
        sheets_instance.spreadsheets().values().clear(
            spreadsheetId=self.googleSheetId,
            range="A1:Z",
            body={},
        ).execute()

        header_row = ["Jailbreak", "Rating"]
        sheets_instance.spreadsheets().values().append(
            spreadsheetId=self.googleSheetId,
            range="A1",
            body={
                "range": "A1:B1",
                "values": [header_row],
                "majorDimension": "ROWS",
            },
            valueInputOption="RAW",
        ).execute()

        # Iterate through the sorted list of jailbreaks and add each jailbreak to the Google Sheet
        for jailbreak, rating in sorted_jailbreaks:
            row_data = [jailbreak, rating]
            sheets_instance.spreadsheets().values().append(
                spreadsheetId=self.googleSheetId,
                range="A:A",
                body={
                    "range": f"A{str(sorted_jailbreaks.index((jailbreak, rating)) + 2)}:B{str(sorted_jailbreaks.index((jailbreak, rating)) + 2)}",
                    "values": [row_data],
                    "majorDimension": "ROWS",
                },
                valueInputOption="RAW",
            ).execute()

        # Return the updatedSheetId
        return GoogleSheetUpdaterOutputDict(updatedSheetId=self.googleSheetId)


load_dotenv()
google_sheet_updater_app = FastAPI()


@google_sheet_updater_app.post("/transform/")
async def transform(
    args: GoogleSheetUpdaterInputDict,
) -> GoogleSheetUpdaterOutputDict:
    google_sheet_updater = GoogleSheetUpdater()
    return google_sheet_updater.transform(args)

