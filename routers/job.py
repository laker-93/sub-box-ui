from http import HTTPStatus

import aiohttp
from fastapi import Request, Header, APIRouter, Cookie
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

@router.get("/job/progress", response_class=HTMLResponse)
async def job_progress(
        request: Request,
        type: str,
        session_id: str | None = Cookie(None),
):
    print(type)
    templates = Jinja2Templates(directory="ui/templates")
    print('progress')

    data = {
        'session_id': session_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('http://0.0.0.0:8002/beets/import/progress', params=data) as response:
            if response.status == HTTPStatus.OK:
                response_json = await response.json()
                print(response_json)
                i = response_json['percentage_complete']
                context = {"request": request, 'percentage_complete': i}
                if i == 0:
                    resp = templates.TemplateResponse("partials/job_progress.html", context)
                    resp.headers['HX-Trigger'] = type
                elif 0 < i < 1:
                    resp = templates.TemplateResponse("partials/job_progress.html", context)
                else:
                    resp = None
                return resp
                #else:
                #    context['reason'] = response_json.get('reason', '')
                #    resp = templates.TemplateResponse("partials/no_uploaded_tracks.html", context)
                #    return resp
            else:
                context = {"request": request}
                print(f'error {response.status} {HTTPStatus.OK}')
                resp = templates.TemplateResponse("partials/failure.html", context)
                return resp
