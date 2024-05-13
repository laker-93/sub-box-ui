from typing import Optional, Dict
from unittest import mock
from http import HTTPStatus

from aiohttp import ClientSession
from dependency_injector.wiring import Provide, inject
from fastapi import Request, Header, APIRouter, Cookie, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from containers import Container

router = APIRouter()
@router.get("/djs", response_class=HTMLResponse)
async def djs(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")
    context = {"request": request}
    return templates.TemplateResponse("djs.html", context)

@router.get("/djs-import", response_class=HTMLResponse)
async def djs(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")
    context = {"request": request}
    return templates.TemplateResponse("dj/djs_import.html", context)

@router.get("/djs-export", response_class=HTMLResponse)
async def djs(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")
    context = {"request": request}
    return templates.TemplateResponse("dj/djs_export.html", context)

@router.get("/rb-import", response_class=HTMLResponse)
async def djs(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")
    context = {"request": request}
    return templates.TemplateResponse("dj/rb_import.html", context)

@router.get("/rb-export", response_class=HTMLResponse)
async def djs(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")
    context = {"request": request}
    return templates.TemplateResponse("dj/rb_export.html", context)

@router.get("/serato-import", response_class=HTMLResponse)
async def djs(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")
    context = {"request": request}
    return templates.TemplateResponse("dj/serato_import.html", context)

@router.get("/serato-export", response_class=HTMLResponse)
async def djs(request: Request, hx_request: Optional[str] = Header(None)):
    templates = Jinja2Templates(directory="ui/templates")
    context = {"request": request}
    return templates.TemplateResponse("dj/serato_export.html", context)

@router.post("/djs/upload/rekordbox", response_class=HTMLResponse)
@inject
async def upload_rekordbox(
        request: Request,
        session_id: str | None = Cookie(None),
        hx_request: Optional[str] = Header(None),
        config: Dict = Provide[Container.config],
        session: ClientSession = Depends(Provide[Container.aiohttp_session])
):
    templates = Jinja2Templates(directory="ui/templates")

    success = False
    context = {"request": request}
    status_code = None
    response_json = ""
    if session_id or isinstance(session, mock.AsyncMock):
        data = {
            'session_id': session_id
        }
        async with session.post(f'http://{config["pymix"]["addr"]}/rekordbox/import', params=data) as response:
            status_code = response.status
            if response.status == HTTPStatus.OK:
                response_json = await response.json()
                success = response_json['success']
                total_n_imported_tracks = response_json['imported_tracks']
                beets_output = response_json['beets_output']
                total_n_tracks_for_import = response_json['n_tracks_for_import']
                context['total_n_imported_tracks'] = total_n_imported_tracks
                context['beets_output'] = beets_output

    if success:
        template = templates.TemplateResponse("partials/job_results.html", context)
    else:
        if total_n_tracks_for_import == 0:
            template = templates.TemplateResponse("partials/empty_uploads.html", context)
        else:
            context["error"] = {
                'status_code': status_code,
                'response': response_json,
                'message': f'Failed to complete import job for session id {session_id}'
            }
            template = templates.TemplateResponse("partials/generic_failure.html", context)
    return template

@router.post("/djs/export/rekordbox", response_class=HTMLResponse)
@inject
async def export_rekordbox(
        request: Request,
        session_id: str | None = Cookie(None),
        local_root: str = Form(...),
        config: Dict = Provide[Container.config],
        session: ClientSession = Depends(Provide[Container.aiohttp_session])
):
    print(local_root)
    templates = Jinja2Templates(directory="ui/templates")

    success = False
    context = {"request": request}
    status_code = None
    response_json = ""
    if session_id or isinstance(session, mock.AsyncMock):
        data = {
            'session_id': session_id,
            'user_root': local_root
        }
        async with session.post(f'http://{config["pymix"]["addr"]}/rekordbox/export', params=data) as response:
            status_code = response.status
            if response.status == HTTPStatus.OK:
                response_json = await response.json()
                success = response_json['success']
                n_beets_tracks = response_json['n_beets_tracks']
                context['n_beets_tracks'] = n_beets_tracks

    if success:
        template = templates.TemplateResponse("partials/rb_export_results.html", context)
    else:
        context["error"] = {
            'status_code': status_code,
            'response': response_json,
            'message': f'Failed to complete export job for session id {session_id}'
        }
        template = templates.TemplateResponse("partials/generic_failure.html", context)
    return template

@router.post("/djs/export/serato", response_class=HTMLResponse)
@inject
async def export_serato(
        request: Request,
        session_id: str | None = Cookie(None),
        local_root: str = Form(...),
        config: Dict = Provide[Container.config],
        session: ClientSession = Depends(Provide[Container.aiohttp_session])
):
    print(local_root)
    templates = Jinja2Templates(directory="ui/templates")

    success = False
    context = {"request": request}
    status_code = None
    response_json = ""
    if session_id or isinstance(session, mock.AsyncMock):
        data = {
            'session_id': session_id,
            'user_root': local_root
        }
        async with session.post(f'http://{config["pymix"]["addr"]}/serato/export', params=data) as response:
            status_code = response.status
            if response.status == HTTPStatus.OK:
                response_json = await response.json()
                print(response_json)
                success = response_json['success']
                n_beets_tracks = response_json['n_beets_tracks']
                context['n_beets_tracks'] = n_beets_tracks

    if success:
        template = templates.TemplateResponse("partials/serato_export_results.html", context)
    else:
        context["error"] = {
            'status_code': status_code,
            'response': response_json,
            'message': f'Failed to complete export job for session id {session_id}'
        }
        template = templates.TemplateResponse("partials/generic_failure.html", context)
    return template

@router.post("/djs/upload/serato", response_class=HTMLResponse)
@inject
async def upload_serato(
        request: Request,
        session_id: str | None = Cookie(None),
        hx_request: Optional[str] = Header(None),
        config: Dict = Provide[Container.config],
        session: ClientSession = Depends(Provide[Container.aiohttp_session])
):
    templates = Jinja2Templates(directory="ui/templates")

    success = False
    context = {"request": request}
    status_code = None
    response_json = ""
    if session_id or isinstance(session, mock.AsyncMock):
        data = {
            'session_id': session_id
        }
        async with session.post(f'http://{config["pymix"]["addr"]}/serato/import', params=data) as response:
            status_code = response.status
            if response.status == HTTPStatus.OK:
                response_json = await response.json()
                success = response_json['success']
                total_n_imported_tracks = response_json['imported_tracks']
                total_n_tracks_for_import = response_json['n_tracks_for_import']
                beets_output = response_json['beets_output']
                context['total_n_imported_tracks'] = total_n_imported_tracks
                context['beets_output'] = beets_output

    if success:
        template = templates.TemplateResponse("partials/job_results.html", context)
    else:
        if total_n_tracks_for_import == 0:
            template = templates.TemplateResponse("partials/empty_uploads.html", context)
        else:
            context["error"] = {
                'status_code': status_code,
                'response': response_json,
                'message': f'Failed to complete import job for session id {session_id}'
            }
            template = templates.TemplateResponse("partials/generic_failure.html", context)
    return template
