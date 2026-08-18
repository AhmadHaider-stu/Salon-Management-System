from fastapi import APIRouter , Request
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix='/logout',tags=['auth'])
templates = Jinja2Templates(directory='app/frontend/templates')

@router.post('')
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/" ,status_code=303)