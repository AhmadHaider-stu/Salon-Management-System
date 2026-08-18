"""
Manual integration test for the salon system's business logic layer.

Flow:
1. Create a client (User + Client)
2. Create an admin user (needed to call admin-gated functions)
3. Register an employee
4. Set the employee's weekly schedule
5. Create a service
6. Assign the employee to the service
7. Book an appointment (inside working hours -> should succeed)
8. Try booking outside working hours (should fail / be rejected)
9. Change appointment status
10. Clean up everything created, in FK-safe order, so the DB ends empty

Run with: python test_flow.py

# CONFIRM: adjust these imports to match your actual project layout —
# I don't have your database.py / models/user.py / models/client.py contents,
# so field names below are best-effort based on what's been shown in our conversation.
"""

from datetime import datetime, time, timedelta

from app.database import SessionLocal  # CONFIRM this is your actual session factory import
from app.enums.enum import Role, DayOfWeek, AppointmentStatus

from app.CRUD.user import add_user, del_user, get_user_by_email
from app.CRUD.client import get_client_by_email
from app.CRUD.employee import get_employee_by_email, del_employee
from app.CRUD.service import get_service_by, del_service
from app.CRUD.employee_service import del_service_by_employee
from app.CRUD.employee_schedule import delete_schedule_for_employee, get_schedule_for_employee
from app.CRUD.appointment import get_client_appointment
from app.CRUD.appointment_service import get_appointment_service_by_appointment

from app.business.login_logic import register_user
from app.business.role_logic import register_employee, make_employee
from app.business.employee_schedule import set_employee_schedule
from app.business.service_logic import create_service
from app.business.employee_logic import assign_employee_services
from app.business.appointment_logic import book_appointment, change_appointment_status


def line(msg):
    print(f"\n--- {msg} ---")


def main():
    db = SessionLocal()
    created = {
        "appointment_id": None,
        "client_email": None,
        "client2_email": None,
        "employee_email": None,
        "service_id": None,
    }

    try:
        # 1. Create a client user (simulating what register_user would do via OAuth)
        line("Creating client user")
        client_email = "test.client@example.com"
        client_user = register_user(
            session=db,
            f_name="test",
            l_name="client",
            oauth_sub="fake-sub-client-001",  # CONFIRM: no real Google token needed since we call business logic directly
            email=client_email,
        )
        created["client_email"] = client_email
        print("Client user created, id:", client_user.id, "client_id:", client_user.client_id)

        # 1b. Second client, needed because a client can't have two active appointments
        #     at all (not just same-day) — so testing the schedule check requires a
        #     separate client, otherwise the client-level DoubleBook check fires first.
        line("Creating second client user")
        client2_email = "test.client2@example.com"
        client2_user = register_user(
            session=db,
            f_name="test",
            l_name="clienttwo",
            oauth_sub="fake-sub-client-002",
            email=client2_email,
        )
        created["client2_email"] = client2_email
        print("Second client user created, id:", client2_user.id, "client_id:", client2_user.client_id)

        # 2. Create an admin (needed to call register_employee-gated actions if you enforce that at API level;
        #    business logic functions here don't all require an admin object directly, so this is optional
        #    unless your register_employee signature needs a current_user — CONFIRM against role_logic.py)
        line("Registering employee")
        employee_email = "test.employee@example.com"
        employee = register_employee(
            session=db,
            f_name="test",
            l_name="employee",
            email=employee_email,
            phone="0500000001",
        )
        created["employee_email"] = employee_email
        db.commit()
        print("Employee created, id:", employee.id)

        # 3. Set employee's weekly schedule (e.g. working Sunday 09:00-18:00)
        line("Setting employee schedule")
        today = datetime.now()
        today_day_name = DayOfWeek(today.strftime('%A').lower())
        schedule_list = [
            {"day_of_week": today_day_name, "start_time": time(9, 0), "end_time": time(18, 0)},
        ]
        set_employee_schedule(session=db, employee_id=employee.id, schedule_list=schedule_list)
        schedule_rows = get_schedule_for_employee(session=db, employee_id=employee.id)
        print("Schedule rows:", [(r.day_of_week, r.start_time, r.end_time) for r in schedule_rows])

        # 4. Create a service
        line("Creating service")
        service = create_service(
            session=db,
            category="HAIR",  # CONFIRM this matches your ServiceCategory enum
            description="test haircut",
            price=50,
            time_duration=30,
        )
        created["service_id"] = service.id
        print("Service created, id:", service.id)

        # 5. Assign employee to service
        line("Assigning employee to service")
        assign_employee_services(session=db, employeeID=employee.id, servicesID=[service.id])
        print("Assigned service", service.id, "to employee", employee.id)

        # 6. Book an appointment inside working hours -> should succeed
        line("Booking appointment inside working hours")
        start_time = datetime.combine(today.date(), time(10, 0))

        class FakeSelection:
            def __init__(self, employee_id, service_id):
                self.employee_id = employee_id
                self.service_id = service_id

        selections = [FakeSelection(employee.id, service.id)]

        book_appointment(
            session=db,
            clientID=client_user.client_id,
            phone="0500000002",
            employee_servicesIDs=selections,
            start_time=start_time,
        )
        appointments = get_client_appointment(session=db, clientID=client_user.client_id)
        assert len(appointments) == 1, "Expected exactly one appointment to be created"
        created["appointment_id"] = appointments[0].id
        print("Booking succeeded, appointment id:", appointments[0].id, "total:", appointments[0].total_price)

        # 7. Try booking outside working hours -> should fail
        # Uses client2 (not client_user) since client_user already has an active
        # appointment and would be blocked by the DoubleBook check first, masking
        # whether the schedule check itself actually works.
        line("Booking appointment OUTSIDE working hours (expect failure)")
        bad_start = datetime.combine(today.date(), time(22, 0))  # outside 09:00-18:00
        try:
            book_appointment(
                session=db,
                clientID=client2_user.client_id,
                phone="0500000003",
                employee_servicesIDs=selections,
                start_time=bad_start,
            )
            print("UNEXPECTED: booking outside working hours succeeded — this should not happen")
        except Exception as e:
            print("Correctly rejected:", type(e).__name__, str(e))
            if type(e).__name__ != "EmployeeBusy":
                print("NOTE: expected rejection reason 'EmployeeBusy' (schedule check), got a different reason — check whether the schedule check actually ran")

        # 8. Change appointment status
        line("Changing appointment status to CONFIRMED")
        change_appointment_status(session=db, appointmentID=created["appointment_id"], status=AppointmentStatus.CONFIRMED)
        appt_services = get_appointment_service_by_appointment(session=db, appointmentID=created["appointment_id"])
        print("AppointmentService statuses:", [a.status for a in appt_services[1]])

        print("\n=== ALL FUNCTIONAL STEPS PASSED ===")

    except Exception as e:
        print("\n!!! TEST FAILED !!!")
        print(type(e).__name__, str(e))
        db.rollback()

    finally:
        # ---- CLEANUP: delete everything created, FK-safe order ----
        line("Cleaning up test data")
        try:
            if created["appointment_id"]:
                appt_services = get_appointment_service_by_appointment(session=db, appointmentID=created["appointment_id"])
                if appt_services[0] == 'OK':
                    for row in appt_services[1]:
                        db.delete(row)
                appointment_row = db.query(__import__('app.models.appointment', fromlist=['Appointment']).Appointment).filter_by(id=created["appointment_id"]).one_or_none()
                if appointment_row:
                    db.delete(appointment_row)
                db.commit()
                print("Deleted appointment + appointment_services")

            if created["employee_email"]:
                status, employee_row = get_employee_by_email(session=db, email=created["employee_email"])
                if status == 'OK':
                    del_service_by_employee(session=db, employeeID=employee_row.id)
                    delete_schedule_for_employee(session=db, employee_id=employee_row.id)
                    del_employee(session=db, employee=employee_row)
                    db.commit()
                    print("Deleted employee + employee_service links + schedule")

            if created["service_id"]:
                status, service_row = get_service_by(session=db, category="HAIR", description="TEST HAIRCUT")
                if status == 'OK':
                    del_service(session=db, serviceID=service_row.id)
                    db.commit()
                    print("Deleted service")

            if created["client_email"]:
                status, user_row = get_user_by_email(session=db, email=created["client_email"])
                if status == 'OK':
                    if user_row.client_id:
                        status2, client_row = get_client_by_email(session=db, email=created["client_email"])
                        if status2 == 'OK':
                            db.delete(client_row)
                    del_user(session=db, userID=user_row.id)
                    db.commit()
                    print("Deleted client user + client record")

            if created["client2_email"]:
                status, user_row = get_user_by_email(session=db, email=created["client2_email"])
                if status == 'OK':
                    if user_row.client_id:
                        status2, client_row = get_client_by_email(session=db, email=created["client2_email"])
                        if status2 == 'OK':
                            db.delete(client_row)
                    del_user(session=db, userID=user_row.id)
                    db.commit()
                    print("Deleted second client user + client record")

            print("\n=== CLEANUP COMPLETE — DB SHOULD BE EMPTY OF TEST DATA ===")

        except Exception as cleanup_error:
            db.rollback()
            print("\n!!! CLEANUP FAILED — MANUAL CHECK NEEDED !!!")
            print(type(cleanup_error).__name__, str(cleanup_error))

        finally:
            db.close()


if __name__ == "__main__":
    main()