from datetime import date as date_type
from fastapi import APIRouter, Depends
from app.dependencies import get_db, require_admin
from app.business.dashboard_logic import get_dashboard_summary, get_stylists_overview, get_appointments_by_hour
from app.business.calendar_logic import get_salon_calendar_day

router = APIRouter(prefix='/dashboard', tags=['dashboard'], dependencies=[Depends(require_admin)])


@router.get('/summary')
def dashboard_summary(db: dict = Depends(get_db)):
    return get_dashboard_summary(session=db)


@router.get('/appointments')
def dashboard_appointments(date: date_type, db: dict = Depends(get_db)):
    return get_salon_calendar_day(session=db, date=date)


@router.get('/stylists')
def dashboard_stylists(db: dict = Depends(get_db)):
    return get_stylists_overview(session=db)


@router.get('/appointments-by-hour')
def dashboard_appointments_by_hour(date: date_type, db: dict = Depends(get_db)):
    return get_appointments_by_hour(session=db, date=date)