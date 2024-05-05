import yaml
import sys
from pathlib import Path

from fastapi import FastAPI
from toredocore.logger import initialise_logger

import constants
from containers import Container
from routers import user, job, about, files, home, upload, djs, process, listen


def create_app():
    app = FastAPI(
        title=constants.title, version=constants.version, description=constants.description
    )

    app.include_router(job.router)
    app.include_router(about.router)
    app.include_router(files.router)
    app.include_router(home.router)
    app.include_router(user.router)
    app.include_router(upload.router)
    app.include_router(djs.router)
    app.include_router(process.router)
    app.include_router(listen.router)
    return app


def create_container(environment="dev"):
    app_config = get_config(environment)

    initialise_logger(
        app_config["application_settings"]["app_name"],
        level=app_config["application_settings"]["logging_level"],
        disable_file_handler=True
    )
    container = Container()
    container.config.from_dict(app_config)
    container.init_resources()
    container.wire(modules=[user, process, job, djs, sys.modules[__name__]])
    return container


def get_config(environment: str) -> dict:
    config_file = Path(__file__).parent / "config" / f"config.{environment}.yaml"
    app_config = yaml.safe_load(config_file.read_text())
    return app_config
