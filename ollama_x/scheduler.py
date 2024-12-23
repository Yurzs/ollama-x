import asyncio
import datetime
import logging

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from ollama_x.config import config
from ollama_x.model import APIServer, OllamaModel

LOG = logging.getLogger(__name__)


jobstores = {"default": MongoDBJobStore(database="ollama_x", host=config.mongo_uri)}


executors = {
    "default": AsyncIOExecutor(),
}

job_defaults = {"coalesce": False, "max_instances": 3}

scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    executors=executors,
    job_defaults=job_defaults,
    timezone=utc,
)


def fake_scheduler() -> AsyncIOScheduler:
    """Fake scheduler to add jobs from outside."""

    scheduler.state = 1
    scheduler.wakeup = lambda: None

    return scheduler


async def check_api(server_id: str) -> None:
    from ollama_x.model.server import APIServer

    server = await APIServer.one(server_id)

    try:
        async with server.ollama_client.list_models() as response:
            if response.status == 200:
                server.last_alive = datetime.datetime.now(utc)

                data = await response.json()
                server.models = data["models"]

                await asyncio.create_task(save_models_info(server))

            else:
                LOG.warning(f"Server {server.url} is inactive")

            server.last_update = datetime.datetime.now(utc)

            await server.commit_changes(fields=["last_alive", "last_update", "models"])
    except Exception as e:
        LOG.exception(f"Error checking server {server.url}", e)


async def check_running_models():
    """Check running models on all servers."""

    from ollama_x.model.server import APIServer

    async for server in APIServer.all_active():
        LOG.debug(f"Checking running models for {server.url}")

        try:
            async with server.ollama_client.list_running_models() as response:
                data = await response.json()
                server.running_models = data["models"]
        except Exception as e:
            LOG.error(f"Error checking running models for {server.url}: {e}")
            server.running_models = []
        finally:
            await server.commit_changes(fields=["running_models"])


async def save_models_info(server: APIServer) -> None:
    """Store model info in the database."""

    for model_base in server.models:
        if not await OllamaModel.find_one(
            model_base["model"],
            model_base["digest"],
            required=False,
        ):
            async with server.ollama_client.show_model_info(
                model_base["model"],
                verbose=True,
            ) as response:
                data = await response.json()

                model = await OllamaModel.create_or_update(
                    model_base["model"],
                    data,
                    model_base["digest"],
                )

                LOG.info(f"Saved `{model.id}` model info.")


def generate_job_id(server_id: str) -> str:
    return f"check_api_{server_id}"


def add_server_job(server_id: str) -> None:
    fake_scheduler().add_job(
        check_api,
        "interval",
        id=generate_job_id(server_id),
        seconds=config.server_check_interval,
        args=[server_id],
    )


def delete_server_job(server_id: str) -> None:
    fake_scheduler().remove_job(generate_job_id(server_id))


async def ensure_jobs():
    from ollama_x.model.server import APIServer

    scheduler.remove_all_jobs()

    async for server in APIServer.all():
        scheduler.add_job(
            check_api,
            "interval",
            id=generate_job_id(server.id),
            seconds=config.server_check_interval,
            args=[server.id],
        )

    scheduler.add_job(
        check_running_models,
        "interval",
        id="check_running_models",
        seconds=config.server_check_interval,
        next_run_time=datetime.datetime.now(utc) + datetime.timedelta(seconds=10),
    )


async def start():
    scheduler.start()

    await ensure_jobs()

    await asyncio.Event().wait()


def main():
    asyncio.run(start())


if __name__ == "__main__":
    main()
