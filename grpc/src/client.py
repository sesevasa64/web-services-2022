import asyncio
from definitions.builds.checker import (
    CheckerStub, CheckRequest, Polygon, Point
)
from grpclib.client import Channel


async def main():
    channel = Channel(host="localhost", port=50051)
    client = CheckerStub(channel)
    polygon = Polygon([Point(x=-1, y=-1), Point(x=1, y=2), Point(x=1, y=-1)])
    point = Point(x=0, y=0)
    response = await client.check(CheckRequest(polygon=polygon, point=point))
    print(response)
    channel.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
