
import os
import yaml
import requests
from bs4 import BeautifulSoup
from typing import List
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from core.abstract_component import AbstractComponent

class JailbreakScraperInputDict(BaseModel):
    pass

class JailbreakScraperOutputDict(BaseModel):
    top_10_prompts: List[str]

class JailbreakScraper(AbstractComponent):
    def __init__(self) -> None:
        super().__init__()

    def transform(self, args: JailbreakScraperInputDict) -> JailbreakScraperOutputDict:
        url = "https://www.jailbreakchat.com/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        prompts = soup.find_all("div", class_="prompt")

        sorted_prompts = sorted(
            prompts,
            key=lambda prompt: float(prompt.find("span", class_="jbscore").text),
            reverse=True
        )

        top_10_prompts = [
            {
                "prompt": p.find("h3").text.strip(),
                "jbscore": float(p.find("span", class_="jbscore").text)
            }
            for p in sorted_prompts[:10]
        ]

        return JailbreakScraperOutputDict(top_10_prompts=top_10_prompts)


load_dotenv()
jailbreak_scraper_app = FastAPI()

@jailbreak_scraper_app.post("/transform/")
async def transform(
    args: JailbreakScraperInputDict,
) -> JailbreakScraperOutputDict:
    jailbreak_scraper = JailbreakScraper()
    return jailbreak_scraper.transform(args)
