import aiohttp
import asyncio

from loguru import logger
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from .dao import RegisterMovieDAO
from .schemas import RegisterMoviePydantic
from parsers.config.database import connection

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Content-Type': 'application/x-www-form-urlencoded',
}

URL = 'https://opendata.mkrf.ru/datatable/register_movies_6013e9b63f75a075a5cb7599/'

PAGE_SIZE = 100
REQUEST_RATE = 10


async def get_page(session: aiohttp.ClientSession, start: int, end: int) -> List[dict]:
    """
    Gets page data of register movies from start to end
    """
    payload = {
        "start": start,
        "end": end,
        "length": str(PAGE_SIZE),
    }

    try:
        async with session.get(url=URL, headers=HEADERS, params=payload) as response:
            if response.status != 200:
                logger.error(f"Request failed: {response.status}")
                return []
            data = await response.json()
            return data.get("data", [])
    except Exception as e:
        logger.exception(f"Page {start}-{end} fetching exception: {e}")
        return []


@connection
async def validate_and_save(items: List[dict], session: AsyncSession = None):
    """
    Validates list of items and saves in database
    """
    valid_items = []

    for item in items:
        try:
            validated = RegisterMoviePydantic.model_validate(item["data"]["general"])
            valid_items.append(validated.model_dump(by_alias=False))
        except Exception as e:
            logger.exception(f"Validation failed for item: {item}. Error: {e}")

    try:
        new_rows = await RegisterMovieDAO.add_many(session, valid_items)
        rows_list = [row.id for row in new_rows]
        logger.info(f"Saved {len(valid_items)} items with id: {rows_list}")
    except Exception as e:
        logger.error(f"Failed to save items: {e}")
        raise


async def start_xhr_parsing(session: aiohttp.ClientSession):
    """
    Fetches paginated data from a remote API using an HTTP session,
    processes the responses, validates the data, and saves it
    """
    async with session.get(url=URL, headers=HEADERS, params={"start": 0, "end": PAGE_SIZE}) as resp:
        data = await resp.json()
        total = data['recordsTotal']

    tasks = []
    for start in range(0, total, PAGE_SIZE):
        end = start + PAGE_SIZE
        tasks.append(get_page(session, start=start, end=end))

    for chunk_start in range(0, len(tasks), REQUEST_RATE):
        chunk = tasks[chunk_start:chunk_start + REQUEST_RATE]
        responses = await asyncio.gather(*chunk)
        for response in responses:
            await validate_and_save(response)
