from http import HTTPStatus

import aiohttp
from aiohttp import ClientSession
from dependency_injector.wiring import Provide, inject
from fastapi import Request, Header, APIRouter, Cookie, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from subbox_landing.containers import Container

router = APIRouter()

@router.get("/job/progress", response_class=HTMLResponse)
@inject
async def job_progress(
        request: Request,
        type: str | None = None,
        session_id: str | None = Cookie(None),
        session: ClientSession = Depends(Provide[Container.aiohttp_session]),
):
    print(type)
    templates = Jinja2Templates(directory="subbox_landing/ui/templates")
    print('progress')

    data = {
        'session_id': session_id
    }

    async with session as session:
        async with session.get('http://pymix:8002/beets/import/progress', params=data) as response:
            if response.status == HTTPStatus.OK:
                response_json = await response.json()
                print(response_json)
                i = response_json['percentage_complete']
                n_tracks_to_import = response_json['n_tracks_to_import']
                context = {"request": request, 'percentage_complete': i}
                if i == 0 and type:
                    resp = templates.TemplateResponse("partials/job_progress.html", context)
                    resp.headers['HX-Trigger'] = type
                elif n_tracks_to_import > 0 and 0 < i < 100:
                    resp = templates.TemplateResponse("partials/job_progress.html", context)
                elif i >= 100:
                    resp = None
                else:
                    # todo need to handle the case of distinguishing between an import about to start (and hence n_tracks_to_import still coming back 0)
                    # todo and the user clicking the process button without any import jobs
                    #    resp = templates.TemplateResponse("partials/no_uploaded_tracks.html", context)
                    resp = templates.TemplateResponse("partials/job_progress.html", context)
                return resp
            else:
                context = {"request": request,
                           "error": {
                               'status_code': response.status,
                               'response': '/beets/import/progress failed'
                           }
                           }
                print(f'error {response.status} {HTTPStatus.OK}')
                resp = templates.TemplateResponse("partials/failure.html", context)
                return resp
