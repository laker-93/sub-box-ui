import asyncio
import logging
from typing import Dict
from unittest import mock

from dependency_injector.wiring import Provide
from uvicorn import Config, Server

from subbox_landing.containers import Container
from subbox_landing.registration import create_app, create_container

logger = logging.getLogger(__name__)


async def main(loop, app_config: Dict = Provide[Container.config]):
    app = create_app()
    config = Config(app=app, loop=loop,
                    host=app_config["application_settings"]["app_host"],
                    port=app_config["application_settings"]["app_port"],
                    log_level=app_config["application_settings"]["logging_level"].lower()
                    )
    server = Server(config)
    server_task = loop.create_task(server.serve())
    await asyncio.gather(server_task)


if __name__ == '__main__':
    container = create_container('dev')
    container.wire(modules=[__name__])
    loop = asyncio.get_event_loop()
    mock_session_mgr = mock.AsyncMock()
    mock_session = mock.MagicMock()
    mock_session_mgr.__aenter__.return_value = mock_session
    mock_response = mock.MagicMock()

    mock_response.status = 200

    get_json_f = asyncio.Future()
    get_json_f.set_result(
        {
            'percentage_complete': 0,
            'n_tracks_to_import': 5
        }
    )


    mock_response.json.return_value = get_json_f
    mock_get_return = mock.AsyncMock()
    mock_get_return.__aenter__.return_value = mock_response
    mock_post_response = mock.MagicMock()
    mock_post_response.status = 200
    async def mock_json_post():
        await asyncio.sleep(5)
        get_json_complete_f = asyncio.Future()
        get_json_complete_f.set_result(
            {
                'percentage_complete': 100,
                'n_tracks_to_import': 5
            }
        )
        mock_response.json.return_value = get_json_complete_f
        return {
            'imported_tracks': 10,
            'beets_output': 'success'
        }
    mock_post_response.json = mock_json_post
    mock_post_return = mock.MagicMock()
    mock_post_return.__aenter__.return_value = mock_post_response
    mock_session.get.return_value = mock_get_return
    mock_session.post.return_value = mock_post_return
    with container.aiohttp_session.override(
        mock_session_mgr
    ):
        try:
            loop.run_until_complete(main(loop))
        except Exception as ex:
            logger.warning(f"loop unexpectedly closed with error {repr(ex)}")
            loop.close()
