from containers import Container
from typing import Optional
from dependency_injector.wiring import Provide, inject
from fastapi import Request, Header, APIRouter, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter()
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
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request, "value": 0}
    import time
    time.sleep(1)
    return templates.TemplateResponse("partials/success.html", context)

@router.put("/contact/1", response_class=HTMLResponse)
async def put_contact(request: Request, hx_request: Optional[str] = Header(None)):
    print('put')
    print(request)
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request}
    if hx_request:
        return templates.TemplateResponse("partials/contact_form.html", context)
    return templates.TemplateResponse("home.html", context)


