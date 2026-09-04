from fastapi import APIRouter, Request, Depends
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.dependencies import get_google_user, get_db
from app.CRUD.user import get_user
from app.frontend.role_routing import get_nav_links, get_role_home
from app.templates import templates
router = APIRouter()

# templates = Jinja2Templates(directory='app/frontend/templates')


@router.get('/')
def index(request: Request, db: dict = Depends(get_db)):
    user_id = request.session.get('user_id')
    if not user_id:
        return templates.TemplateResponse(request=request, name="login.html", context={})

    status, user = get_user(session=db, userID=user_id)
    if status == 'FAIL':
        request.session.clear()
        return templates.TemplateResponse(request=request, name="login.html", context={})

    return RedirectResponse(get_role_home(user.role))


@router.get('/home')
def home(request: Request, db: dict = Depends(get_db), userID: int = Depends(get_google_user)):
    status, user = get_user(session=db, userID=userID)
    if status == 'FAIL':
        return RedirectResponse('/')

    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"user": user, "active_page": "home", "nav_links": get_nav_links(user.role), "brand_href": "/home"}
    )


@router.get('/book')
def book_page(request: Request, db: dict = Depends(get_db), userID: int = Depends(get_google_user)):
    status, user = get_user(session=db, userID=userID)
    if status == 'FAIL':
        return RedirectResponse('/')

    return templates.TemplateResponse(
        request=request,
        name="book.html",
        context={"user": user, "active_page": "book", "nav_links": get_nav_links(user.role), "brand_href": "/home"}
    )


@router.get('/my-appointments')
def my_appointments_page(request: Request, db: dict = Depends(get_db), userID: int = Depends(get_google_user)):
    status, user = get_user(session=db, userID=userID)
    if status == 'FAIL':
        return RedirectResponse('/')

    return templates.TemplateResponse(
        request=request,
        name="my_appointments.html",
        context={"user": user, "active_page": "appointments", "nav_links": get_nav_links(user.role), "brand_href": "/home"}
    )