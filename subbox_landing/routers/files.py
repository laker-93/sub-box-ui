import os
from typing import Optional
from fastapi import Request, Header, APIRouter
from fastapi.responses import FileResponse

router = APIRouter()
@router.get("/imgs/spin", response_class=FileResponse)
async def spin(request: Request, hx_request: Optional[str] = Header(None)):
    file_location = os.getcwd() + "/subbox_landing/ui/templates/imgs/spin.svg"
    return FileResponse(file_location)

@router.get("/imgs/bars", response_class=FileResponse)
async def spin(request: Request, hx_request: Optional[str] = Header(None)):
    file_location = os.getcwd() + "/subbox_landing/ui/templates/imgs/bars.svg"
    return FileResponse(file_location)

@router.get("/imgs/upload", response_class=FileResponse)
async def spin(request: Request, hx_request: Optional[str] = Header(None)):
    file_location = os.getcwd() + "/subbox_landing/ui/templates/imgs/upload.png"
    return FileResponse(file_location)

@router.get("/imgs/process", response_class=FileResponse)
async def spin(request: Request, hx_request: Optional[str] = Header(None)):
    file_location = os.getcwd() + "/subbox_landing/ui/templates/imgs/process.png"
    return FileResponse(file_location)

@router.get("/imgs/listen", response_class=FileResponse)
async def spin(request: Request, hx_request: Optional[str] = Header(None)):
    file_location = os.getcwd() + "/subbox_landing/ui/templates/imgs/listen.png"
    return FileResponse(file_location)
