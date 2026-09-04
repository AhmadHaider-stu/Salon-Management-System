from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from app.dependencies import get_db, get_current_user
from app.enums.enum import Role
from app.frontend.role_routing import get_nav_links, get_role_home
from app.templates import templates
router = APIRouter()
# templates = Jinja2Templates(directory='app/frontend/templates')


@router.get('/reception/calendar')
def reception_calendar(request: Request, user=Depends(get_current_user)):
    if user.role not in (Role.RECEPTION, Role.ADMIN):
        return RedirectResponse(get_role_home(user.role))
    return templates.TemplateResponse(request=request, name="calendar.html", context={
        "user": user,
        "active_page": "calendar",
        "nav_links": get_nav_links(user.role),
        "brand_href": get_role_home(user.role),
        "is_staff": True,
        "own_employee_id": None,
    })


@router.get('/employee/calendar')
def employee_calendar(request: Request, user=Depends(get_current_user)):
    if user.role != Role.EMPLOYEE:
        return RedirectResponse(get_role_home(user.role))
    return templates.TemplateResponse(request=request, name="calendar.html", context={
        "user": user,
        "active_page": "calendar",
        "nav_links": get_nav_links(user.role),
        "brand_href": get_role_home(user.role),
        "is_staff": False,
        "own_employee_id": user.employee_id,
    })


@router.get('/admin/roles')
def admin_roles(request: Request, user=Depends(get_current_user)):
    if user.role != Role.ADMIN:
        return RedirectResponse(get_role_home(user.role))
    return templates.TemplateResponse(request=request, name="admin_roles.html", context={
        "user": user,
        "active_page": "dashboard",
        "nav_links": get_nav_links(user.role),
        "brand_href": get_role_home(user.role),
    })


@router.get('/admin/dashboard')
def admin_dashboard(request: Request, user=Depends(get_current_user)):
    if user.role != Role.ADMIN:
        return RedirectResponse(get_role_home(user.role))
    return templates.TemplateResponse(request=request, name="dashboard.html", context={
        "user": user,
        "active_page": "dashboard",
        "nav_links": get_nav_links(user.role),
        "brand_href": get_role_home(user.role),
    })


# Shared across every role — now real
@router.get('/me')
def me_page(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse(request=request, name="me.html", context={
        "user": user,
        "active_page": "me",
        "nav_links": get_nav_links(user.role),
        "brand_href": get_role_home(user.role),
    })


@router.get('/reception/employees')
def reception_employees(request: Request, user=Depends(get_current_user)):
    if user.role not in (Role.RECEPTION, Role.ADMIN):
        return RedirectResponse(get_role_home(user.role))
    return templates.TemplateResponse(request=request, name="reception_employees.html", context={
        "user": user,
        "active_page": "employees",
        "nav_links": get_nav_links(user.role),
        "brand_href": get_role_home(user.role),
    })


@router.get('/reception/clients')
def reception_clients(request: Request, user=Depends(get_current_user)):
    if user.role not in (Role.RECEPTION, Role.ADMIN):
        return RedirectResponse(get_role_home(user.role))
    return templates.TemplateResponse(request=request, name="reception_clients.html", context={
        "user": user,
        "active_page": "clients",
        "nav_links": get_nav_links(user.role),
        "brand_href": get_role_home(user.role),
    })


@router.get('/reception/appointments')
def reception_appointments_redirect(request: Request, user=Depends(get_current_user)):
    # Merged into /reception/calendar - reschedule/reprice now live there for any appointment.
    return RedirectResponse('/reception/calendar')


@router.get('/reception/employees')
def reception_employees(request: Request, user=Depends(get_current_user)):
    if user.role not in (Role.RECEPTION, Role.ADMIN):
        return RedirectResponse(get_role_home(user.role))
    return templates.TemplateResponse(request=request, name="reception_employees.html", context={
        "user": user,
        "active_page": "employees",
        "nav_links": get_nav_links(user.role),
        "brand_href": get_role_home(user.role),
    })


@router.get('/reception/clients')
def reception_clients(request: Request, user=Depends(get_current_user)):
    if user.role not in (Role.RECEPTION, Role.ADMIN):
        return RedirectResponse(get_role_home(user.role))
    return templates.TemplateResponse(request=request, name="reception_clients.html", context={
        "user": user,
        "active_page": "clients",
        "nav_links": get_nav_links(user.role),
        "brand_href": get_role_home(user.role),
    })


@router.get('/reception/services')
def reception_services(request: Request, user=Depends(get_current_user)):
    if user.role not in (Role.RECEPTION, Role.ADMIN):
        return RedirectResponse(get_role_home(user.role))
    return templates.TemplateResponse(request=request, name="reception_services.html", context={
        "user": user,
        "active_page": "services",
        "nav_links": get_nav_links(user.role),
        "brand_href": get_role_home(user.role),
    })


@router.get('/stylists')
def stylists_page(request: Request, user=Depends(get_current_user)):
    if user.role != Role.CLIENT:
        return RedirectResponse(get_role_home(user.role))
    return templates.TemplateResponse(request=request, name="stylists.html", context={
        "user": user,
        "active_page": "stylists",
        "nav_links": get_nav_links(Role.CLIENT),
        "brand_href": "/home",
    })


@router.get('/services')
def client_services_page(request: Request, user=Depends(get_current_user)):
    if user.role != Role.CLIENT:
        return RedirectResponse(get_role_home(user.role))
    return templates.TemplateResponse(request=request, name="services.html", context={
        "user": user,
        "active_page": "services",
        "nav_links": get_nav_links(Role.CLIENT),
        "brand_href": "/home",
    })