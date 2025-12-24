from molotov import scenario, setup, teardown

from clients.postgresql import PostgresClient
from core.config import settings
from core.helpers import generate_current_date_str

pg_client = None


@setup()
async def init_worker(worker_num, args):
    global pg_client
    pg_client = PostgresClient(settings.db_url)


@teardown()
async def shutdown_worker(worker_num, args):
    global pg_client
    if pg_client:
        pg_client.close()


@scenario(weight=50)
async def insert_document_scenario(session):
    pg_client.insert_document()


@scenario(weight=50)
async def count_signatures_scenario(session):
    pg_client.get_signature_count_for_day(generate_current_date_str())
