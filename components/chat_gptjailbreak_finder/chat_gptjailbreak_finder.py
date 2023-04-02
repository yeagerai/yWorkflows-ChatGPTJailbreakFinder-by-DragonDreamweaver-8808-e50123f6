
import typing
from typing import Any
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from core.workflows.abstract_workflow import AbstractWorkflow

class ChatGPTJailbreakFinderIn(BaseModel):
    GoogleApiKey: str

class ChatGPTJailbreakFinderOut(BaseModel):
    UpdatedGoogleSheetId: str

class ChatGPTJailbreakFinder(AbstractWorkflow):
    def __init__(self) -> None:
        super().__init__()

    async def transform(
        self, args: ChatGPTJailbreakFinderIn, callbacks: typing.Any
    ) -> ChatGPTJailbreakFinderOut:
        results_dict = await super().transform(args=args, callbacks=callbacks)
        updated_google_sheet_id = results_dict[list(results_dict.keys())[-1]].google_sheet_id
        out = ChatGPTJailbreakFinderOut(UpdatedGoogleSheetId=updated_google_sheet_id)
        return out

load_dotenv()
chatgpt_jailbreak_finder_app = FastAPI()

@chatgpt_jailbreak_finder_app.post("/transform/")
async def transform(
    args: ChatGPTJailbreakFinderIn,
) -> ChatGPTJailbreakFinderOut:
    chatgpt_jailbreak_finder = ChatGPTJailbreakFinder()
    return await chatgpt_jailbreak_finder.transform(args, callbacks=None)

