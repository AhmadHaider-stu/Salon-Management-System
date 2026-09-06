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
app.add_middleware(SessionMiddleware, secret_key=os.getenv('SESSION_SECRET',None
                                                           ,https_only = True
                                                           ))
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







