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

@router.get("/imgs/rb-import-enable-xml", response_class=FileResponse)
async def rb_import_enable_xml(request: Request, hx_request: Optional[str] = Header(None)):
    file_location = os.getcwd() + "/subbox_landing/ui/templates/imgs/RB-import-enable-xml.png"
    return FileResponse(file_location)
@router.get("/imgs/rb-import-set-xml-path", response_class=FileResponse)
async def rb_import_set_xml_path(request: Request, hx_request: Optional[str] = Header(None)):
    file_location = os.getcwd() + "/subbox_landing/ui/templates/imgs/RB-import-set-xml-path.png"
    return FileResponse(file_location)
@router.get("/imgs/rb-backup", response_class=FileResponse)
async def rb_backup(request: Request, hx_request: Optional[str] = Header(None)):
    file_location = os.getcwd() + "/subbox_landing/ui/templates/imgs/RB-backup.png"
    return FileResponse(file_location)

@router.get("/imgs/rb-backup-music-files", response_class=FileResponse)
async def rb_backup_music_files(request: Request, hx_request: Optional[str] = Header(None)):
    file_location = os.getcwd() + "/subbox_landing/ui/templates/imgs/RB-backup-music-files.png"
    return FileResponse(file_location)

@router.get("/imgs/player-screenshot", response_class=FileResponse)
async def rb_backup_music_files(request: Request, hx_request: Optional[str] = Header(None)):
    file_location = os.getcwd() + "/subbox_landing/ui/templates/imgs/player-screenshot.png"
    return FileResponse(file_location)
