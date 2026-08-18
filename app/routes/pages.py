from fastapi import APIRouter, Request , Depends
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.dependencies import get_google_user , get_db
from app.CRUD.user import get_user


router = APIRouter()

# CHANGE THE KEYYYYYYYYYYYY
templates = Jinja2Templates(directory='app/frontend/templates')


@router.get('/')
def index(request: Request):
    user = request.session.get('user_id')
    if user:
        return RedirectResponse('home')

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


@router.get('/home')
def home(request: Request , db : dict = Depends(get_db),userID : int = Depends(get_google_user)):
    status, user = get_user(session=db , userID=userID)
    if status == 'FAIL':
        return RedirectResponse('/')

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"user": user}
    )


