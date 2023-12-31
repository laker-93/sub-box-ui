from http import HTTPStatus
from typing import Optional
from unittest import mock

from aiohttp import ClientSession
from dependency_injector.wiring import Provide, inject
from fastapi import Request, Header, APIRouter, Cookie, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from subbox_landing.containers import Container

router = APIRouter()


@router.get("/process", response_class=HTMLResponse)
async def process(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="subbox_landing/ui/templates")
    response = templates.TemplateResponse('process.html', {'request': request})
    return response


@router.post("/process/beets", response_class=HTMLResponse)
@inject
async def process_beets(
        request: Request,
        session_id: str | None = Cookie(None),
        hx_request: Optional[str] = Header(None),
        session: ClientSession = Depends(Provide[Container.aiohttp_session]),
):
    templates = Jinja2Templates(directory="subbox_landing/ui/templates")

    success = False
    context = {"request": request}
    status_code = None
    response_json = ""
    if session_id or isinstance(session, mock.AsyncMock):
        data = {
            'session_id': session_id
        }
        async with session.post('http://pymix:8002/beets/import', params=data) as response:
            status_code = response.status
            if response.status == HTTPStatus.OK:
                response_json = await response.json()
                success = True
                total_n_imported_tracks = response_json['imported_tracks']
                beets_output = response_json['beets_output']
                context['total_n_imported_tracks'] = total_n_imported_tracks
                context['beets_output'] = beets_output

    if success:
        template = templates.TemplateResponse("partials/job_results.html", context)
    else:
        context["error"] = {
            'status_code': status_code,
            'response': response_json,
            'message': f'Failed to complete import job for session id {session_id}'
        }
        template = templates.TemplateResponse("partials/generic_failure.html", context)
    return template

