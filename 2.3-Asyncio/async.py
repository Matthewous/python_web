import asyncio
import aiohttp
from pprint import pprint
from more_itertools import chunked

CHUNK_SIZE = 10

async def get_people(session, people_id):
    
    async with session.get(f'https://swapi.dev/api/people/{people_id}') as responce:
        return await responce.json()


async def main():
    session = aiohttp.ClientSession()
    coros = (get_people(session, i) for i in range(1,20))
    for coros_chunk in chunked(coros, CHUNK_SIZE):
        result = await asyncio.gather(*coros_chunk)
        pprint(result)
    await session.close()

asyncio.run(main())