from fastapi import APIRouter, Depends, HTTPException

from app.business.client_logic import *
from app.dependencies import require_receptionist_or_admin, get_db
from app.schemas.client import ClientEdit

router = APIRouter(prefix='/client', tags=['client'])


@router.get('', dependencies=[Depends(require_receptionist_or_admin)], summary='Get all clients')
def list_all_clients(db: dict = Depends(get_db)):
    return get_all_clients(session=db)


@router.put('/{clientID}/edit', dependencies=[Depends(require_receptionist_or_admin)], summary='Edit client info')
def edit_client(clientID: int, data: ClientEdit, db: dict = Depends(get_db)):
    try:
        return alter_client(session=db, clientID=clientID, data=data)
    except InvalidPhoneNumber:
        raise HTTPException(status_code=400, detail='Invalid phone number')
    except NotFoundClient:
        raise HTTPException(status_code=404, detail='Client not found')


@router.get('/{clientID}/appointments', summary='Get all client appointments', dependencies=[Depends(require_receptionist_or_admin)])
def get_client_appointments(clientID: int, db: dict = Depends(get_db)):
    try:
        return get_appointments_by_client(session=db, clientID=clientID)
    except NotFoundClient:
        raise HTTPException(status_code=404, detail='Client not found')