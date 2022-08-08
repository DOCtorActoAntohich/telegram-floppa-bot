from aiohttp import ClientSession


class GetCatThatDoesNotExist:
    @staticmethod
    async def execute() -> bytes:
        async with ClientSession() as session, session.get('https://thiscatdoesnotexist.com/') as response:
            if response.status != 200:
                raise ValueError(f'Invalid response ({response.status}): {await response.text()}.')

            return await response.content.read()
