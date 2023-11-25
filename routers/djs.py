from typing import Optional
import aiohttp
from http import HTTPStatus
from fastapi import Request, Header, APIRouter, Cookie, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
@router.get("/djs", response_class=HTMLResponse)
async def djs(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")
    context = {"request": request}
    return templates.TemplateResponse("djs.html", context)

@router.post("/djs/upload/rekordbox", response_class=HTMLResponse)
async def upload_rekordbox(
        request: Request,
        session_id: str | None = Cookie(None),
        hx_request: Optional[str] = Header(None)
):
    templates = Jinja2Templates(directory="ui/templates")

    success = False
    context = {"request": request}
    status_code = None
    response_json = ""
    if session_id:
        data = {
            'session_id': session_id
        }
        async with aiohttp.ClientSession() as session:
            async with session.post('http://0.0.0.0:8002/rekordbox/import', params=data) as response:
                status_code = response.status
                if response.status == HTTPStatus.OK:
                    response_json = await response.json()
                    print(response_json)
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

@router.post("/djs/export/rekordbox", response_class=HTMLResponse)
async def export_rekordbox(
        request: Request,
        session_id: str | None = Cookie(None),
        local_root: str = Form(...),
):
    print(local_root)
    templates = Jinja2Templates(directory="ui/templates")

    success = False
    context = {"request": request}
    status_code = None
    response_json = ""
    if session_id:
        data = {
            'session_id': session_id,
            'user_root': local_root
        }
        async with aiohttp.ClientSession() as session:
            async with session.post('http://0.0.0.0:8002/rekordbox/export', params=data) as response:
                status_code = response.status
                if response.status == HTTPStatus.OK:
                    response_json = await response.json()
                    print(response_json)
                    success = True
                    total_n_exported_tracks = response_json['exported_tracks']
                    context['total_n_exported_tracks'] = total_n_exported_tracks

    if success:
        template = templates.TemplateResponse("partials/job_results.html", context)
    else:
        context["error"] = {
            'status_code': status_code,
            'response': response_json,
            'message': f'Failed to complete export job for session id {session_id}'
        }
        template = templates.TemplateResponse("partials/generic_failure.html", context)
    return template
