from datetime import date as date_type
from fastapi import APIRouter, Depends
from app.dependencies import get_db, require_receptionist_or_admin
from app.business.calendar_logic import get_salon_calendar_day, get_salon_calendar_month

router = APIRouter(prefix='/calendar', tags=['calendar'], dependencies=[Depends(require_receptionist_or_admin)])


@router.get('/day')
def salon_calendar_day(date: date_type, db: dict = Depends(get_db)):
    return get_salon_calendar_day(session=db, date=date)


@router.get('/month')
def salon_calendar_month(year: int, month: int, db: dict = Depends(get_db)):
    return get_salon_calendar_month(session=db, year=year, month=month)