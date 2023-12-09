from typing import Optional
from fastapi import Request, Header, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()


@router.get("/listen", response_class=HTMLResponse)
async def upload(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="subbox_landing/ui/templates")
    response = templates.TemplateResponse('listen.html', {'request': request})
    return response


@router.get("/listen/player", response_class=HTMLResponse)
async def filebrowser(request: Request, hx_request: Optional[str] = Header(None)):
    print('redirect')
    templates = Jinja2Templates(directory="subbox_landing/ui/templates")
    data = {'msg': 'Logged in successfully'}
    response = templates.TemplateResponse('home.html', {'request': request, 'data': data})
    response.headers['HX-Redirect'] = 'https://player.sub-box.net/player/#'
    return response


