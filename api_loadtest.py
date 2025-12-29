from datetime import datetime
from http import HTTPStatus

from molotov import scenario

from core.constants import _API, SIGN_RESPONSE_MODEL_FIELDS
from core.decorators import debug_print_out
from core.helpers import generate_document_payload


@scenario(weight=25)
@debug_print_out
async def get_index_page(session):
    async with session.get(_API) as response:
        assert response.status == HTTPStatus.OK


@scenario(weight=25)
@debug_print_out
async def post_sign(session):

    payload = generate_document_payload()

    async with session.post(f"{_API}/api/sign", json=payload) as response:
        data = await response.json()
        assert response.status == HTTPStatus.OK

        for key in SIGN_RESPONSE_MODEL_FIELDS:
            assert key in data

        assert data["document_id"] == payload["document_id"]
        assert "signature_value" in data
        datetime.fromisoformat(data["signed_at"].replace("Z", "+00:00"))


@scenario(weight=25)
@debug_print_out
async def get_sign_ping(session):
    async with session.get(f"{_API}/api/sign/ping") as response:
        data = await response.json()
        assert response.status == HTTPStatus.OK
        assert data["status"] == "ok"


@scenario(weight=25)
@debug_print_out
async def get_cache_test(session):
    async with session.get(f"{_API}/api/cache/cache-test") as response:
        data = await response.json()
        assert response.status == HTTPStatus.OK
        assert data["cached_value"] == "Hello, Redis!"
