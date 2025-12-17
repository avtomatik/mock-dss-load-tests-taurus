import json
import random
import time
from urllib.parse import urlparse

import aio_pika
import aioredis
import asyncpg

from core.config import settings
from core.constants import SQL_INSERT_DOCUMENT, SQL_SELECT_COUNT
from core.helpers import (
    generate_current_date_str,
    generate_random_content,
    generate_random_id,
)

# =============================================================================
# Shared clients per worker
# =============================================================================


class Clients:
    pg_conn = None
    redis = None
    rabbit_conn = None
    rabbit_channel = None
    rabbit_queue = "test_queue"


clients = Clients()


async def setup(args):
    """Runs once per Molotov worker"""
    # =========================================================================
    # PostgreSQL (asyncpg)
    # =========================================================================
    clients.pg_conn = await asyncpg.connect(settings.db_url)

    # =========================================================================
    # Redis (aioredis)
    # =========================================================================
    clients.redis = await aioredis.create_redis_pool(
        settings.cache_url, encoding="utf-8"
    )

    # =========================================================================
    # RabbitMQ (aio-pika)
    # =========================================================================
    parsed = urlparse(settings.mq_url)
    clients.rabbit_conn = await aio_pika.connect_robust(
        host=parsed.hostname,
        port=parsed.port,
        login=parsed.username,
        password=parsed.password,
    )
    clients.rabbit_channel = await clients.rabbit_conn.channel()
    await clients.rabbit_channel.declare_queue(
        clients.rabbit_queue, durable=True
    )


async def teardown(args):
    """Runs once per Molotov worker"""
    if clients.pg_conn:
        await clients.pg_conn.close()

    if clients.redis:
        clients.redis.close()

    if clients.rabbit_conn:
        await clients.rabbit_conn.close()


# =============================================================================
# Scenario
# =============================================================================


async def scenario(session):
    """
    One iteration = one weighted operation
    We emulate Locust task weights via random choice
    """
    choice = random.choices(
        population=[
            "query_db",
            "insert_db",
            "publish_message",
            "redis_ops",
        ],
        weights=[3, 2, 4, 3],
        k=1,
    )[0]

    start = time.perf_counter()

    try:
        if choice == "query_db":
            result = await clients.pg_conn.fetchrow(
                SQL_SELECT_COUNT, generate_current_date_str()
            )
            count = result[0] if result else 0

        elif choice == "insert_db":
            await clients.pg_conn.execute(
                SQL_INSERT_DOCUMENT,
                generate_random_id(),
                generate_random_content(),
            )

        elif choice == "publish_message":
            payload = {
                "ts": time.perf_counter(),
                "payload": "sync_test",
            }
            body = json.dumps(payload).encode()

            await clients.rabbit_channel.default_exchange.publish(
                aio_pika.Message(
                    body=body,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key=clients.rabbit_queue,
            )

        elif choice == "redis_ops":
            key = f"test:{int(time.time() * 1000)}"
            await clients.redis.set(key, "value", expire=120)
            val = await clients.redis.get(key)

        elapsed = (time.perf_counter() - start) * 1000
        session.record_success(choice, elapsed, 0)
    except Exception as exc:
        elapsed = (time.perf_counter() - start) * 1000
        session.record_failure(choice, elapsed, str(exc))
        raise
