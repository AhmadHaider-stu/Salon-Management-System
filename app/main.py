from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes.login import router as login_router
from app.routes.pages import router as pages_router
from app.routes.logout import router as logout_router
from app.routes.user import router as user_router
from app.routes.service import router as service_router
from app.routes.employee import router as employee_router
from app.routes.appointment import router as appointment_router
from app.routes.role_manipulation import router as role_router
from app.routes.client import router as client_router
from app.routes.calendar import router as calendar_router
from app.routes.dashboard import router as dashboard_router
from app.routes.staff_pages import router as staff_router
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.business.reminders import send_pending_reminders
from datetime import datetime
import os 
import json
from app.i18n.strings import t, STRINGS
from zoneinfo import ZoneInfo
from app.i18n.strings import t, STRINGS, CATEGORY_LABELS,STATUS_LABELS , ROLE_LABELS
now = datetime.now(ZoneInfo("Asia/Amman"))

from app.database import Base, engine
import app.models

Base.metadata.create_all(engine)
from app.database import Base, engine
import app.models

Base.metadata.create_all(engine)


_bootstrap_email = os.getenv('ADMIN_BOOTSTRAP_EMAIL')
if _bootstrap_email:
    from app.CRUD.user import get_user_by_email
    from app.business.role_logic import make_employee, make_admin
    from app.enums.enum import Role
    _bootstrap_db = SessionLocal()
    try:
        status, user = get_user_by_email(session=_bootstrap_db, email=_bootstrap_email)
        if status == 'OK' and user.role != Role.ADMIN:
            user.role = Role.ADMIN  
            _bootstrap_db.commit()
            make_employee(session=_bootstrap_db, current_user=user, userID=user.id)
            user.role = Role.ADMIN
            _bootstrap_db.commit()
            make_admin(session=_bootstrap_db, current_user=user, userID=user.id)
            _bootstrap_db.commit()
            print(f"Bootstrapped admin: {_bootstrap_email}")
        elif status == 'FAIL':
            print(f"ADMIN_BOOTSTRAP_EMAIL set but no user found yet with email {_bootstrap_email}")
    except Exception as e:
        _bootstrap_db.rollback()
        print(f"Admin bootstrap failed: {e}")
    finally:
        _bootstrap_db.close()


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)
def run_reminder_check():
    print("REMINDER CHECK RUNNING", datetime.now())
    db = SessionLocal()
    try:
        send_pending_reminders(session=db)
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(run_reminder_check, 'interval', minutes=2)
scheduler.start()

# CHANGE THE KEYYYYYYYYYYYY
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv('SESSION_SECRET', None),
    # https_only=True
)
app.mount('/static', StaticFiles(directory='app/frontend/static'), name='static')

templates = Jinja2Templates(directory='app/frontend/templates')


templates.env.globals['t'] = t
templates.env.globals['STRINGS_JSON'] = json.dumps(STRINGS, ensure_ascii=False)
templates.env.globals['CATEGORY_LABELS_JSON'] = json.dumps(CATEGORY_LABELS, ensure_ascii=False)
templates.env.globals['STATUS_LABELS_JSON'] = json.dumps(STATUS_LABELS, ensure_ascii=False)
templates.env.globals['ROLE_LABELS_JSON'] = json.dumps(ROLE_LABELS, ensure_ascii=False)


app.include_router(login_router)
app.include_router(pages_router)
app.include_router(logout_router)
app.include_router(user_router)
app.include_router(service_router)
app.include_router(employee_router)
app.include_router(appointment_router)
app.include_router(role_router)
app.include_router(client_router)
app.include_router(calendar_router)
app.include_router(dashboard_router)
app.include_router(staff_router)







