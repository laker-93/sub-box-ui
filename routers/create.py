from typing import Optional
from fastapi import Request, Header, APIRouter, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
@router.post("/create", response_class=HTMLResponse)
async def create(
        request: Request,
        firstName: str = Form(...),
        lastName: str = Form(...),
        hx_request: Optional[str] = Header(None)
):
    print('create')
    print(request)
    print('name')
    print(firstName)
    print(lastName)
    templates = Jinja2Templates(directory="ui/templates")

    context = {"request": request, "value": 0}
    return templates.TemplateResponse("partials/job_progress.html", context)