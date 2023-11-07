import aiohttp
import logging
from http import HTTPStatus

from containers import Container
from typing import Optional
from dependency_injector.wiring import Provide, inject
from fastapi import Request, Header, APIRouter, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()

logger = logging.getLogger(__name__)
@router.get("/user/signupform", response_class=HTMLResponse)
async def signup_form(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request}
    return templates.TemplateResponse("partials/signup_form.html", context)

@router.get("/user/loginform", response_class=HTMLResponse)
async def login_form(request: Request,
                hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request}
    return templates.TemplateResponse("partials/login_form.html", context)

@router.post("/user/login", response_class=HTMLResponse)
async def login(request: Request,
                username: str = Form(...),
                password: str = Form(...),
                hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request}
    # get count of tracks in sub box then use these to format the table.
    return templates.TemplateResponse("partials/table.html", context)


@router.post("/user/create", response_class=HTMLResponse)
@inject
async def create(
        request: Request,
        config: dict = Depends(Provide[Container.config]),
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        hx_request: Optional[str] = Header(None)
):
    host = config['py_mix']['host']
    port = config['py_mix']['port']
    print(f'host {host} port {port}')
    print(f'username {username} password {password} email {email}')
    data = {
        'username': username,
        'password': password
    }
    error = {}
    async with aiohttp.ClientSession() as session:
        async with session.post('http://0.0.0.0:8002/create_user', params=data) as response:
            error['status_code'] = response.status
            if response.status == HTTPStatus.OK:
                response_json = await response.json()
                print(response_json)
                if not response_json.get('success'):
                    error['response'] = response_json.get('reason')
                    template = 'partials/failure.html'
                else:
                    template = 'partials/success.html'
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

    context = {"request": request, "error": error}
    return templates.TemplateResponse(template, context)

@router.put("/contact/1", response_class=HTMLResponse)
async def put_contact(request: Request, hx_request: Optional[str] = Header(None)):
    print('put')
    print(request)
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request}
    if hx_request:
        return templates.TemplateResponse("partials/contact_form.html", context)
    return templates.TemplateResponse("home.html", context)


