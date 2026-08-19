from app.enums.enum import Role

CLIENT_NAV = [
    {"key": "home", "href": "/home", "label": "Home", "icon": "home"},
    {"key": "book", "href": "/book", "label": "Book", "icon": "book"},
    {"key": "appointments", "href": "/my-appointments", "label": "My visits", "icon": "appointments"},
    {"key": "services", "href": "/services", "label": "Services", "icon": "services"},
    {"key": "me", "href": "/me", "label": "Me", "icon": "me"},
]

EMPLOYEE_NAV = [
    {"key": "calendar", "href": "/employee/calendar", "label": "Calendar", "icon": "calendar"},
    {"key": "me", "href": "/me", "label": "Me", "icon": "me"},
]

# Reception and admin share the same nav. Add employees/clients/appointments
# back to this list one at a time as each is actually built.
RECEPTION_NAV = [
    {"key": "calendar", "href": "/reception/calendar", "label": "Calendar", "icon": "calendar"},
    {"key": "appointments", "href": "/reception/appointments", "label": "Appointments", "icon": "appointments"},
    {"key": "employees", "href": "/reception/employees", "label": "Employees", "icon": "employees"},
    {"key": "clients", "href": "/reception/clients", "label": "Clients", "icon": "clients"},
    {"key": "services", "href": "/reception/services", "label": "Services", "icon": "services"},
    {"key": "me", "href": "/me", "label": "Me", "icon": "me"},
]

ADMIN_NAV = [
    {"key": "dashboard", "href": "/admin/dashboard", "label": "Dashboard", "icon": "dashboard"},
    {"key": "calendar", "href": "/reception/calendar", "label": "Calendar", "icon": "calendar"},
    {"key": "appointments", "href": "/reception/appointments", "label": "Appointments", "icon": "appointments"},
    {"key": "employees", "href": "/reception/employees", "label": "Employees", "icon": "employees"},
    {"key": "clients", "href": "/reception/clients", "label": "Clients", "icon": "clients"},
    {"key": "services", "href": "/reception/services", "label": "Services", "icon": "services"},
    {"key": "me", "href": "/me", "label": "Me", "icon": "me"},
]

ROLE_HOME = {
    Role.CLIENT: "/home",
    Role.EMPLOYEE: "/employee/calendar",
    Role.RECEPTION: "/reception/calendar",
    Role.ADMIN: "/reception/calendar",
}

ROLE_NAV = {
    Role.CLIENT: CLIENT_NAV,
    Role.EMPLOYEE: EMPLOYEE_NAV,
    Role.RECEPTION: RECEPTION_NAV,
    Role.ADMIN: ADMIN_NAV,
}


def get_role_home(role):
    return ROLE_HOME.get(role, "/home")


def get_nav_links(role):
    return ROLE_NAV.get(role, CLIENT_NAV)