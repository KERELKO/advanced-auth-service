from blacksheep.testing import TestClient
from blacksheep import Application


app = Application()


async def test_api_auth():
    _ = TestClient(app)
