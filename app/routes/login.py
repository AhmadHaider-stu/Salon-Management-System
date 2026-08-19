from fastapi import APIRouter, Request, Depends, Form
from authlib.integrations.starlette_client import OAuthError
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from app.auth.google import oauth
from app.business.login_logic import *
from app.dependencies import get_db
from app.frontend.role_routing import get_role_home


router = APIRouter(prefix='/login', tags=['auth'])

templates = Jinja2Templates(directory='app/frontend/templates')


@router.get("")
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)


@router.get('/auth', name='auth')
async def auth(request: Request, db: dict = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(request=request, name="login.html", context={"error": e.error})

    google_user = token.get('userinfo')
    if not google_user:
        return templates.TemplateResponse(request=request, name="login.html", context={"error": "no_userinfo"})

    existing = get_user_by_sub(session=db, sub=google_user['sub'])
    if existing is not None:
        try:
            current_user = login_user(session=db, oauth_sub=google_user['sub'])
        except IsBlocked:
            return templates.TemplateResponse(request=request, name='login.html', context={'error': 'blocked'})
        request.session['user_id'] = current_user.id
        return RedirectResponse(get_role_home(current_user.role), status_code=303)

    request.session['pending_registration'] = {
        'f_name': google_user.get('given_name'),
        'l_name': google_user.get('family_name'),
        'email': google_user['email'],
        'sub': google_user['sub'],
    }
    return RedirectResponse("/login/complete-phone", status_code=303)


@router.get('/complete-phone')
async def complete_phone_form(request: Request):
    if 'pending_registration' not in request.session:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(request=request, name="complete_phone.html", context={})


@router.post('/complete-phone')
async def complete_phone_submit(request: Request, phone: str = Form(...), db: dict = Depends(get_db)):
    pending = request.session.get('pending_registration')
    if pending is None:
        return RedirectResponse("/login", status_code=303)

    try:
        user = register_user(session=db, f_name=pending['f_name'], l_name=pending['l_name'],
                              email=pending['email'], oauth_sub=pending['sub'], phone=phone)
    except InvalidPhoneNumber:
        return templates.TemplateResponse(request=request, name="complete_phone.html", context={"error": "invalid_phone"})
    except UsedPhoneNumber:
        return templates.TemplateResponse(request=request, name="complete_phone.html", context={"error": "phone_taken"})

    del request.session['pending_registration']
    request.session['user_id'] = user.id
    return RedirectResponse(get_role_home(user.role), status_code=303)