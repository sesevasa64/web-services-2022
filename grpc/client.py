import asyncio
from definitions.builds.checker import CheckerStub, CheckRequest, Polygon, Point
from grpclib.client import Channel


async def main():
    channel = Channel(host="127.0.0.1", port=50051)
    service = CheckerStub(channel)
    polygon = Polygon([Point(x=-1, y=-1), Point(x=1, y=2), Point(x=1, y=-1)])
    point = Point(x=0, y=0)
    response = await service.check(CheckRequest(polygon=polygon, point=point))
    print(response)
    channel.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
