# -*- encoding: utf-8 -*-
import json
import base64
from io import BytesIO
from collections import Counter
import time
import typing
import os
import matplotlib.pyplot as plt

import pandas as pd
import asyncio
import aiohttp

import requests
from dagster import asset, AssetExecutionContext, MaterializeResult, MetadataValue
from . import resources


async def fetch_one_story(client, url, sem) -> typing.Awaitable[dict]:
    """

    Args:
        client (aiohttp.Client.ClientSession):
        url (str):
        sem (asyncio.Semaphore):
    Returns:

    """
    async with sem:
        async with client.get(url) as resp:
            story_json = await resp.json()
    return story_json


async def fetch_stories(context: AssetExecutionContext, story_ids):
    def new_async_client():
        return aiohttp.ClientSession()

    story_url = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    awaitable_stories = []
    start_time = time.time()
    sem = asyncio.Semaphore(10)
    async with new_async_client() as client:
        async with asyncio.TaskGroup() as tg:
            for story_id in story_ids:
                awaitable_stories.append(tg.create_task(
                    fetch_one_story(client, story_url.format(item_id=story_id), sem),
                ))
    await client.close()
    res = await asyncio.gather(*awaitable_stories)
    context.log.info(f"done within {time.time() - start_time}")
    return res


@asset(description="Collect hackernews topstory ids")
def asset_top_story_ids() -> None:
    hackernews_topstories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    resp = requests.get(hackernews_topstories_url, timeout=5000)
    try:
        topstories = resp.json()[:100]
    except Exception as e:
        print("can not get top stories", e)
        topstories = []
    os.makedirs("data", exist_ok=True)
    with open("data/topstory_ids.json", "w", encoding="utf-8") as f:
        json.dump(topstories, f)


@asset(deps=[asset_top_story_ids], description="Fetch top stories by ID")
def asset_top_stories(context: AssetExecutionContext) -> MaterializeResult:
    with open("data/topstory_ids.json") as f:
        story_ids: list[int] = json.load(f)

    result = asyncio.run(fetch_stories(context, story_ids))
    # result = []
    # story_url = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    # for story_id in story_ids:
    #     story_json = requests.get(story_url.format(item_id=story_id)).json()
    #     result.append(story_json)
    #     if len(result) % 20 == 0:
    #         print(f"Got {len(result)} item so far....")
    df = pd.DataFrame(result)
    df.to_csv("data/topstories.csv")
    return MaterializeResult(
        metadata={
            "num_of_record": len(df),
            "preview": MetadataValue.md(df.head().to_markdown())
        }
    )


@asset(deps=[asset_top_stories], description="Get frequency words")
def asset_most_frequent_words(context: AssetExecutionContext) -> MaterializeResult:
    stopwords = ["a", "the", "an", "of", "to", "in", "for", "and", "with", "on", "is"]
    top_stories: pd.DataFrame = pd.read_csv('data/topstories.csv')
    work_count = {}
    for raw_title in top_stories['title']:
        title = raw_title.lower()
        for word in title.split():
            clean_word = word.strip(".,–!?:;()[]'\"-")
            if clean_word and clean_word not in stopwords:
                work_count[clean_word] = work_count.get(clean_word, 0) + 1
    context.log.debug(f"Total work counter {json.dumps(work_count, indent=4)}")
    top_words: dict[str, int] = dict(Counter(work_count).most_common(25))
    with open("data/most_frequent_words.json", "w") as f:
        json.dump(top_words, f, ensure_ascii=False)

    plt.figure(figsize=(10, 6))
    plt.bar(list(top_words.keys()), list(top_words.values()))
    plt.xticks(rotation=45, ha="right")  # * rotate x-axis label 45 degrees
    plt.title("Top 25 words in Hacker News titles")
    plt.tight_layout()
    buff = BytesIO()
    plt.savefig(buff, format="png")
    img_data = base64.b64encode(buff.getvalue())
    img_md_data = f"![img](data:image/png;base64,{img_data.decode()})"

    return MaterializeResult(
        metadata={
            "plot": MetadataValue.md(img_md_data),
        }
    )


@asset
def asset_signup(hackernews_api: resources.DataGeneratorResource) -> MaterializeResult:
    signups_raw = hackernews_api.get_signups()
    df = pd.DataFrame(signups_raw)
    df.to_csv("data/signups.csv")
    return MaterializeResult(
        metadata={
            "Record Count": len(signups_raw),
            "Preview": MetadataValue.md(df.head(10).to_markdown()),
            # "Preview": MetadataValue.table(df.head(10).values.tolist()),
            "Earliest Signup": df["registered_at"].min(),
            "Latest Signup": df["registered_at"].max(),
        }
    )
