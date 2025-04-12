import asyncio

from aiohttp import ClientSession

from register_movies.utils import start_xhr_parsing


async def main():
    async with ClientSession() as session:
        await start_xhr_parsing(session)


if __name__ == '__main__':
    asyncio.run(main())
