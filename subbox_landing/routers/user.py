import aiohttp
import logging
from http import HTTPStatus

from aiohttp import ClientSession
from starlette.responses import JSONResponse

from typing import Optional, Dict
from dependency_injector.wiring import Provide, inject
from fastapi import Request, Header, APIRouter, Form, Depends, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from containers import Container

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/user/signupform", response_class=HTMLResponse)
@inject
async def signup_form(
        request: Request,
        session_id: str | None = Cookie(None),
        hx_request: Optional[str] = Header(None),
        config: Dict = Provide[Container.config],
        session: ClientSession = Depends(Provide[Container.aiohttp_session])
):
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request}
    success = False

    if session_id:
        try:
            username = await _get_username_by_session_id(config["pymix"]["addr"], session_id, session)
        except Exception:
            logger.error('error getting user by session id', exc_info=True)
        else:
            context.update(
                {
                    "user": {
                        "username": username
                    }
                }
            )
            success = True
    if success:
        template = templates.TemplateResponse("partials/logged_in.html", context)
    else:
        template = templates.TemplateResponse("partials/signup_form.html", context)
    return template


async def _get_username_by_session_id(addr: str, session_id: str, session: ClientSession) -> str:
    data = {
        'session_id': session_id
    }
    async with session.get(f'http://{addr}/user/get_by_session_id', params=data) as response:
        if response.status == HTTPStatus.OK:
            response_json = await response.json()
            try:
                user = response_json['user']
            except KeyError:
                logger.error(f'error extracting user from {response_json}', exc_info=True)
                raise
            else:
                try:
                    username = user['username']
                except KeyError:
                    logger.error(f'error extracting username from {user}', exc_info=True)
                    raise
    return username


@router.get("/user/loginform", response_class=HTMLResponse)
@inject
async def login_form(request: Request,
                     session_id: str | None = Cookie(None),
                     hx_request: Optional[str] = Header(None),
                     config: Dict = Provide[Container.config],
                     session: ClientSession = Depends(Provide[Container.aiohttp_session])
                     ):
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request}
    success = False
    if session_id:
        try:
            username = await _get_username_by_session_id(config["pymix"]["addr"], session_id, session)
        except Exception:
            logger.error('error getting user by session id', exc_info=True)
        else:
            context.update(
                {
                    "user": {
                        "username": username
                    }
                }
            )
            success = True
    if success:
        template = templates.TemplateResponse("partials/logged_in.html", context)
    else:
        template = templates.TemplateResponse("partials/login_form.html", context)
    return template


@router.post("/user/login", response_class=HTMLResponse)
@inject
async def login(
        request: Request,
        session_id: str | None = Cookie(None),
        username: str = Form(...),
        password: str = Form(...),
        hx_request: Optional[str] = Header(None),
        config: dict = Depends(Provide[Container.config]),
        session: ClientSession = Depends(Provide[Container.aiohttp_session]),
):
    print(f'username {username} password {password}')
    print(f'got cookie {session_id}')
    data = {
        'username': username,
        'password': password,
        # aiohttp does not support sending a None param
        'session_id': 'none' if not session_id else session_id
    }
    error = {}
    success = False
    async with session.post(f'http://{config["pymix"]["addr"]}/user/login', params=data) as response:
        error['status_code'] = response.status
        if response.status == HTTPStatus.OK:
            response_json = await response.json()
            session_id = response.cookies.get('session_id').value
            print(response_json)
            template = 'partials/logged_in.html'
            success = True
        else:
            print(f'error {response.status} {HTTPStatus.OK}')
            try:
                response_json = await response.json()
            except Exception:
                logger.error(f'failed to decode response {response}', exc_info=True)
                response_json = ""
            template = 'partials/failure.html'
            error['response'] = response_json

    templates = Jinja2Templates(directory="ui/templates")
    if success:
        context = {
            "request": request,
            "user": {
                "username": username
            }
        }
        response = templates.TemplateResponse(template, context)
        print(f'setting cookie to {session_id}')
        response.set_cookie(key='session_id', value=session_id, httponly=True)
    else:
        context = {"request": request, "error": error}
        response = templates.TemplateResponse(template, context)
    return response

@router.post("/user/create", response_class=HTMLResponse)
@inject
async def create(
        request: Request,
        session_id: str | None = Cookie(None),
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        dj: str | None = Form(True),
        hx_request: Optional[str] = Header(None),
        config: dict = Depends(Provide[Container.config]),
        session: ClientSession = Depends(Provide[Container.aiohttp_session]),
):
    templates = Jinja2Templates(directory="ui/templates")
    if any(c.isupper() for c in username):
        template = 'partials/username_uppercase.html'
        context = {"request": request, "username": username}
        response = templates.TemplateResponse(template, context)
        return response

    print(f'username {username} password {password} session id {session_id} dj {dj}')
    data = {
        'username': username,
        'password': password,
        'email': email,
        'dj': str(dj)
    }
    error = {}
    success = False
    async with session.post(f'http://{config["pymix"]["addr"]}/user/create', params=data) as response:
        error['status_code'] = response.status
        if response.status == HTTPStatus.OK:
            session_id = response.cookies.get('session_id')
            if session_id:
                session_id = session_id.value
                template = 'partials/success.html'
            else:
                template = 'partials/max_users.html'
            success = True
        else:
            print(f'error {response.status} {HTTPStatus.OK}')
            try:
                response_json = await response.json()
            except Exception:
                logger.error(f'failed to decode response {response}', exc_info=True)
                response_json = ""
            template = 'partials/failure.html'
            error['response'] = response_json

    context = {"request": request}
    if success:
        if session_id:
            #response = JSONResponse(content="ok", status_code=HTTPStatus.OK)
            response = templates.TemplateResponse(template, context)
            print(f'setting cookie to {session_id}')
            response.set_cookie(key='session_id', value=session_id, httponly=True)
        else:
            response = templates.TemplateResponse(template, context)
    else:
        context = {"request": request, "error": error}
        response = templates.TemplateResponse(template, context)

    return response


@router.put("/contact/1", response_class=HTMLResponse)
async def put_contact(request: Request, hx_request: Optional[str] = Header(None)):
    print('put')
    print(request)
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request}
    if hx_request:
        return templates.TemplateResponse("partials/contact_form.html", context)
    return templates.TemplateResponse("home.html", context)
