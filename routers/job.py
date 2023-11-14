from typing import Optional
from fastapi import Request, Header, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
i = 0

@router.get("/job/progress", response_class=HTMLResponse)
async def job_progress(request: Request, hx_request: Optional[str] = Header(None)):
    global i
    context = {"request": request, 'value': i}
    templates = Jinja2Templates(directory="ui/templates")
    print('progress')
    print(i)


    i += 20
    if hx_request:
        if i <= 100:
            resp = templates.TemplateResponse("partials/job_progress.html", context)
            resp.headers['HX-Trigger'] = 'start-job'
            return resp
