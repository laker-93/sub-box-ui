from typing import Optional
from fastapi import Request, Header, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
@router.get("/contact/1/edit", response_class=HTMLResponse)
async def edit_contact(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request}
    if hx_request:
        return templates.TemplateResponse("partials/contact_form.html", context)
    return templates.TemplateResponse("index.html", context)

@router.get("/contact/1", response_class=HTMLResponse)
async def get_contact(request: Request, hx_request: Optional[str] = Header(None)):
    print('get')
    print(request)
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


@router.put("/contact/1", response_class=HTMLResponse)
async def put_contact(request: Request, hx_request: Optional[str] = Header(None)):
    print('put')
    print(request)
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request}
    if hx_request:
        return templates.TemplateResponse("partials/contact_form.html", context)
    return templates.TemplateResponse("index.html", context)


