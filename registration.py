import yaml
import sys
from pathlib import Path

from fastapi import FastAPI
from toredocore.logger import initialise_logger

import constants
from routers import index, contact, create, job


def create_app():
    app = FastAPI(
        title=constants.title, version=constants.version, description=constants.description
    )

    app.include_router(create.router)
    app.include_router(index.router)
    app.include_router(contact.router)
    app.include_router(job.router)
    return app


def create_container(environment="dev") -> dict:
    app_config = get_config(environment)

    initialise_logger(
        app_config["application_settings"]["app_name"],
        level=app_config["application_settings"]["logging_level"],
        disable_file_handler=True
    )
    return app_config


def get_config(environment: str) -> dict:
    config_file = Path(__file__).parent / "config" / f"config.{environment}.yaml"
    app_config = yaml.safe_load(config_file.read_text())
    return app_config
