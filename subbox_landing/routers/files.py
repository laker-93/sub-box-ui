import os
from typing import Optional
from fastapi import Request, Header, APIRouter
from fastapi.responses import FileResponse

router = APIRouter()
@router.get("/imgs/spin", response_class=FileResponse)
async def spin(request: Request, hx_request: Optional[str] = Header(None)):
    file_location = os.getcwd() + "/subbox_landing/ui/templates/imgs/spin.svg"
    return FileResponse(file_location)