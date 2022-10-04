import pytest
from random import randint
from src.server import CheckerService
from definitions.builds.checker import (
    CheckerStub, CheckRequest, Polygon, Point, Result
)
from grpclib.testing import ChannelFor


def create_polygon(n: int):
    """Create a random polygon with "n" points
    Args:
        n (int): number of points
    Returns:
        Polygon: random polygon
    """
    points = [Point(x=randint(0, 10), y=randint(0, 10)) for _ in range(n)]
    return Polygon(points=points)


def non_polygons():
    """Parameterization for test with list of incorrect polygons
    Returns:
        List[Polygon]: incorrect polygons
    """
    return [(create_polygon(i), Result.ERROR) for i in range(3)]


@pytest.mark.asyncio
async def test_grpc_service():
    async with ChannelFor([CheckerService()]) as channel:
        client = CheckerStub(channel)
        polygon = Polygon([
            Point(x=-1, y=-1), Point(x=1, y=2), Point(x=1, y=-1)
        ])
        request = CheckRequest(polygon=polygon, point=Point(x=0, y=0))
        response = await client.check(request)
        assert response.result == Result.OK and response.is_inside is True
        request = CheckRequest(polygon=polygon, point=Point(x=10, y=10))
        response = await client.check(request)
        assert response.result == Result.OK and response.is_inside is False


@pytest.mark.asyncio
@pytest.mark.parametrize("polygon, expected", non_polygons())
async def test_grpc_service_input(polygon: Polygon, expected: Result):
    async with ChannelFor([CheckerService()]) as channel:
        client = CheckerStub(channel)
        request = CheckRequest(polygon=polygon, point=Point(x=0, y=0))
        response = await client.check(request)
        assert response.result == expected
