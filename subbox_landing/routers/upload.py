from typing import Optional
from fastapi import Request, Header, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()


@router.get("/upload", response_class=HTMLResponse)
async def upload(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")
    response = templates.TemplateResponse('upload.html', {'request': request})
    return response

@router.get("/download", response_class=HTMLResponse)
async def download(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")
    response = templates.TemplateResponse('download.html', {'request': request})
    return response

@router.get("/upload/filebrowser", response_class=HTMLResponse)
async def filebrowser(request: Request, hx_request: Optional[str] = Header(None)):
    print('redirect')
    templates = Jinja2Templates(directory="ui/templates")
    data = {'msg': 'Logged in successfully'}
    response = templates.TemplateResponse('home.html', {'request': request, 'data': data})
    response.headers['HX-Redirect'] = 'https://browser.sub-box.net/browser'
    return response


