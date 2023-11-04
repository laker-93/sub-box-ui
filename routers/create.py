from typing import Optional
from dependency_injector.wiring import Provide, inject
from fastapi import Request, Header, APIRouter, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from containers import Container

router = APIRouter()
@router.post("/create", response_class=HTMLResponse)
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
    #return templates.TemplateResponse("partials/upload.html", context)