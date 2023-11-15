from http import HTTPStatus
from typing import Optional

import aiohttp
from fastapi import Request, Header, APIRouter, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()


@router.get("/process", response_class=HTMLResponse)
async def process(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")
    response = templates.TemplateResponse('process.html', {'request': request})
    return response


@router.post("/process/test", response_class=HTMLResponse)
async def process_test(
        request: Request
):
    templates = Jinja2Templates(directory="ui/templates")

    print('process start')
    success = False
    context = {"request": request}
    import asyncio
    await asyncio.sleep(10)
    success = True


    print('process success')
    if success:
        template = templates.TemplateResponse("partials/success.html", context)
    else:
        template = templates.TemplateResponse("partials/failure.html", context)
    return template


@router.post("/process/beets", response_class=HTMLResponse)
async def process_beets(
        request: Request,
        session_id: str | None = Cookie(None),
        hx_request: Optional[str] = Header(None)
):
    templates = Jinja2Templates(directory="ui/templates")

    success = False
    context = {"request": request}
    if session_id:
        data = {
            'session_id': session_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post('http://0.0.0.0:8002/beets/import', params=data) as response:
                if response.status == HTTPStatus.OK:
                    response_json = await response.json()
                    print(response_json)
                    success = True

    if success:
        template = templates.TemplateResponse("partials/success.html", context)
    else:
        template = templates.TemplateResponse("partials/failure.html", context)
    return template

