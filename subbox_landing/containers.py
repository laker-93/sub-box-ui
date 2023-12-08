import aiohttp
from dependency_injector import containers, providers

from factories.aiohttp_session_resource import init_aiohttp_session


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    aiohttp_session = providers.Resource(
        init_aiohttp_session,
        connector=providers.Factory(
            aiohttp.TCPConnector, verify_ssl=False
        )
    )
