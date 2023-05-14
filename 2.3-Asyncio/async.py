import aiohttp
import asyncio
from more_itertools import chunked
from models import engine, Session, Base, SwapiPeople
from aiohttp import ClientSession
import requests

CHUNK_SIZE = 10

async def chunked_async(async_iter, size):
    buffer = []
    while True:
        try:
            item = await async_iter.__anext__()
        except StopAsyncIteration:
            if buffer:
                yield buffer
            break
        buffer.append(item)
        if len(buffer) == size:
            yield buffer
            buffer = []


async def get_person(people_id: int, session: ClientSession):
    print(f'begin {people_id}')
    async with session.get(f'https://swapi.dev/api/people/{people_id}') as response:
        json_data = await response.json()
    print(f'end {people_id}')
    return json_data


async def get_people():
    async with ClientSession() as session:
        for chunk in chunked(range(1, 20), CHUNK_SIZE):
            coroutines = [get_person(people_id=i, session=session) for i in chunk]
            results = await asyncio.gather(*coroutines)
            for item in results:
                yield item


async def paste_to_db(results):
    async with Session() as session:
        session.add_all([SwapiPeople(name=item['name'],
                                     birth_year=item['birth_year'],
                                     eye_color=item['eye_color'],
                                     films=', '.join([film['title']
                                                      for film in [requests.get(ind).json()
                                                                   for ind in item['films']]]),
                                     species=', '.join([specy['name']
                                                        for specy in [requests.get(ind).json()
                                                                      for ind in item['species']]]),
                                     vehicles=', '.join([vehicle['name']
                                                         for vehicle in [requests.get(ind).json()
                                                                         for ind in item['vehicles']]]),
                                     starships=', '.join([starship['name']
                                                          for starship in [requests.get(ind).json()
                                                                           for ind in item['starships']]]),
                                     gender=item['gender'],
                                     hair_color=item['hair_color'],
                                     height=item['height'],
                                     homeworld=item['homeworld'],
                                     mass=item['mass'],
                                     skin_color=item['skin_color']
                                     ) for item in results if 'detail' not in item])
        await session.commit()


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    async for chunk in chunked_async(get_people(), CHUNK_SIZE):
        asyncio.create_task(paste_to_db(chunk))

    tasks = set(asyncio.all_tasks()) - {asyncio.current_task()}
    for task in tasks:
        await task


asyncio.run(main())