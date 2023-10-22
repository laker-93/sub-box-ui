import asyncio
import logging
from uvicorn import Config, Server

from registration import create_app, create_container

logger = logging.getLogger(__name__)


async def main(loop):
    app = create_app()
    app_config = create_container()
    config = Config(app=app, loop=loop,
                    host=app_config["application_settings"]["app_host"],
                    port=app_config["application_settings"]["app_port"],
                    log_level=app_config["application_settings"]["logging_level"].lower()
                    )
    server = Server(config)
    server_task = loop.create_task(server.serve())
    await asyncio.gather(server_task)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    except Exception as ex:
        logger.warning(f"loop unexpectedly closed with error {repr(ex)}")
        loop.close()
