# from parsera import Parsera
# import os
# os.environ["PARSERA_API_KEY"] = "615eda737a4c9af2ad5026386f2065f9"

# url = "https://news.ycombinator.com/"
# elements = {
#     "Title": "News title",
#     "Points": "Number of points",
#     "Comments": "Number of comments",
# }

# scraper = Parsera()
# result = scraper.run(url=url, elements=elements)
# print(result)

import asyncio
import requests
from scraper import get_html_soup
from dotenv import load_dotenv
import os
from langchain_ollama import ChatOllama
from parsera import Parsera

load_dotenv()
PARSERA_API_KEY = os.getenv("PARSERA_API_KEY")


def get_weight_text_ore(url):
    soup = get_html_soup(url)
    # print(soup)
    tab_description = soup.find("div", class_="tabs-contents")
    if tab_description:
        for line in tab_description.stripped_strings:
            if "weight" in line.lower():
                ore = line
                return ore


def get_weight_from_text(text):
    url = "https://api.parsera.org/v1/parse"
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": PARSERA_API_KEY
    }
    data = {
        "content": text,
        "attributes": [
            {"name": "Weight", "description": "weight of the battery in grams (just the number)"}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()
    weight = response_json['data'][0]["Weight"]
    weight = weight.replace(' ', '').strip()
    return weight


async def test_local(url):
    elements = {
        "weight": "weight of the battery in grams (just the number)"
    }
    llm = ChatOllama(
        model="qwen2.5:14b",
        temperature=0,
    )
    scraper = Parsera(model=llm)
    result = await scraper.arun(url=url, elements=elements)
    return result


result = asyncio.run(test_local("https://rotorvillage.ca/smc-hcl-rs-22-2v-1600mah-lipo-xt60/"))
print(result)
