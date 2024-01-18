from http import HTTPStatus
from typing import Dict

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
        config: Dict = Provide[Container.config]
):
    templates = Jinja2Templates(directory="ui/templates")

    data = {
        'session_id': session_id
    }

    async with session.get(f'http://{config["pymix"]["addr"]}/beets/import/progress', params=data) as response:
        if response.status == HTTPStatus.OK:
            response_json = await response.json()
            percentage_complete = response_json['percentage_complete']
            n_tracks_to_import = response_json['n_tracks_to_import']
            n_tracks_imported = response_json['n_tracks_imported']
            import_in_progress = response_json['import_in_progress']
            context = {"request": request, 'percentage_complete': percentage_complete,
                       "n_tracks_to_import": n_tracks_to_import,
                       "n_tracks_imported": n_tracks_imported}
            if not import_in_progress and type:
                resp = templates.TemplateResponse("partials/staging_in_progress.html", context)
                # this will kick off the import job
                resp.headers['HX-Trigger'] = type
            elif import_in_progress and percentage_complete == 0:
                resp = templates.TemplateResponse("partials/staging_in_progress.html", context)
            elif n_tracks_to_import > 0 and 0 < percentage_complete <= 100:
                resp = templates.TemplateResponse("partials/job_progress.html", context)
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
            resp = templates.TemplateResponse("partials/failure.html", context)
            return resp
