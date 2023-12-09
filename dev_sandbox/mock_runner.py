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


def _make_mock_import_responses():
    mock_import_progress_response = mock.MagicMock()
    mock_import_progress_response.status = 200
    mock_import_progress_json_1 = asyncio.Future()
    mock_import_progress_json_1.set_result(
        {
            'percentage_complete': 0,
            'n_tracks_to_import': 0,
            'import_in_progress': False,
        }
    )
    mock_import_progress_json_2 = asyncio.Future()
    mock_import_progress_json_2.set_result(
        {
            'percentage_complete': 0,
            'n_tracks_to_import': 50,
            'import_in_progress': True,
        }
    )
    mock_import_progress_json_3 = asyncio.Future()
    mock_import_progress_json_3.set_result(
        {
            'percentage_complete': 2,
            'n_tracks_to_import': 50,
            'import_in_progress': True,
        }
    )
    mock_import_progress_json_4 = asyncio.Future()
    mock_import_progress_json_4.set_result(
        {
            'percentage_complete': 5,
            'n_tracks_to_import': 50,
            'import_in_progress': True,
        }
    )
    mock_import_progress_json_5 = asyncio.Future()
    mock_import_progress_json_5.set_result(
        {
            'percentage_complete': 50,
            'n_tracks_to_import': 50,
            'import_in_progress': True,
        }
    )
    mock_import_progress_json_6 = asyncio.Future()
    mock_import_progress_json_6.set_result(
        {
            'percentage_complete': 100,
            'n_tracks_to_import': 50,
            'import_in_progress': True,
        }
    )
    mock_import_progress_json_7 = asyncio.Future()
    mock_import_progress_json_7.set_result(
        {
            'percentage_complete': 100,
            'n_tracks_to_import': 50,
            'import_in_progress': True,
        }
    )
    mock_import_progress_json_8 = asyncio.Future()
    mock_import_progress_json_8.set_result(
        {
            'percentage_complete': 100,
            'n_tracks_to_import': 50,
            'import_in_progress': False,
        }
    )
    mock_import_progress_response.json.side_effect = [
        mock_import_progress_json_1,
        mock_import_progress_json_2,
        mock_import_progress_json_3,
        mock_import_progress_json_4,
        mock_import_progress_json_5,
        mock_import_progress_json_6,
        mock_import_progress_json_7,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
        mock_import_progress_json_8,
    ]
    mock_import_progress_return = mock.AsyncMock()
    mock_import_progress_return.__aenter__.return_value = mock_import_progress_response
    mock_import_response = mock.MagicMock()
    mock_import_response.status = 200

    async def mock_import_json():
        await asyncio.sleep(5)
        get_json_complete_f = asyncio.Future()
        get_json_complete_f.set_result(
            {
                'percentage_complete': 100,
                'n_tracks_to_import': 5,
                'import_in_progress': True
            }
        )
        mock_import_progress_response.json.return_value = get_json_complete_f
        await asyncio.sleep(5)
        return {
            'imported_tracks': 10,
            'beets_output': 'success'
        }

    mock_import_response.json = mock_import_json
    mock_import_return = mock.MagicMock()
    mock_import_return.__aenter__.return_value = mock_import_response
    return mock_import_progress_return, mock_import_return


if __name__ == '__main__':
    container = create_container('dev')
    container.wire(modules=[__name__])
    loop = asyncio.get_event_loop()
    mock_session_mgr = mock.AsyncMock()
    mock_session = mock.MagicMock()
    mock_session_mgr.__aenter__.return_value = mock_session

    mock_import_progress_return, mock_import_return = _make_mock_import_responses()

    def mock_get(url, **kwargs):
        if url.endswith('beets/import/progress'):
            return mock_import_progress_return
    def mock_post(url, **kwargs):
        if url.endswith('beets/import'):
            return mock_import_return

    mock_session.get = mock_get
    mock_session.post = mock_post
    with container.aiohttp_session.override(
        mock_session_mgr
    ):
        try:
            loop.run_until_complete(main(loop))
        except Exception as ex:
            logger.warning(f"loop unexpectedly closed with error {repr(ex)}")
            loop.close()
