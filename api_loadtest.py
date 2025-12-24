from datetime import datetime
from http import HTTPStatus

from molotov import scenario

from core.constants import _API
from core.helpers import generate_random_id


@scenario(weight=25)
async def get_index_page(session):
    async with session.get(_API) as response:
        assert response.status == HTTPStatus.OK


@scenario(weight=25)
async def post_sign(session):

    document_id = generate_random_id()

    payload = {
        "document_id": document_id,
        "payload": "Lorem ipsum dolor sit amet consectetuer",
    }
    async with session.post(f"{_API}/api/sign", json=payload) as response:
        data = await response.json()
        assert response.status == HTTPStatus.OK

        for key in [
            "signature_id",
            "document_id",
            "signed_at",
            "signature_value",
        ]:
            assert key in data

        assert data["document_id"] == payload["document_id"]
        assert "signature_value" in data
        datetime.fromisoformat(data["signed_at"])


@scenario(weight=25)
async def get_sign_ping(session):
    async with session.get(f"{_API}/api/sign/ping") as response:
        data = await response.json()
        assert response.status == HTTPStatus.OK
        assert data["status"] == "ok"


@scenario(weight=25)
async def get_cache_test(session):
    async with session.get(f"{_API}/api/cache/cache-test") as response:
        assert response.status == HTTPStatus.OK
        assert response["cached_value"] == "Hello, Redis!"
