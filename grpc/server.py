import asyncio
from grpclib.server import Server
from definitions.builds.checker import CheckerBase, CheckRequest, CheckResponse, Result


class CheckerService(CheckerBase):
    async def check(self, check_request: "CheckRequest") -> "CheckResponse":
        """Check if point is inside a polygon
        Args:
            check_request (CheckRequest): Polygon and testing point.
        Returns:
            True for success, False otherwise.
        """
        print(check_request)
        points = check_request.polygon.points
        point = check_request.point
        is_inside = False
        for i, p_i in enumerate(points):
            p_j = points[(i + 1) % len(points)]
            if not (p_i.y <= point.y < p_j.y or p_j.y <= point.y < p_i.y):
                continue
            x_cross = (point.y - p_j.y) / (p_j.y - p_i.y) * (p_j.x - p_i.x) + point.x
            if x_cross < point.x:
                is_inside = not is_inside
        return CheckResponse(result=Result.OK, is_inside=is_inside)


async def main():
    server = Server([CheckerService()])
    await server.start("localhost", 50051)
    await server.wait_closed()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
