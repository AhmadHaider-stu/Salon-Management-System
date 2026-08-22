from app.business.employee_logic import *
from app.business.role_logic import *
from app.CRUD.client import *
from app.dependencies import get_db
db = next(get_db())

# user = get_user(session=db , userID = 1)[1]
# user.role = Role.ADMIN
# db.commit()
# make_employee(session=db , current_user=user,userID=1 )
# user.role = Role.ADMIN
# db.commit()
# make_admin(session=db , current_user=user , userID = 1)
# # del_user(session=db ,userID=1)
del_client(session= db , clientID=3)
db.commit()
