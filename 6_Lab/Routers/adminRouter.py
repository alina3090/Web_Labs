from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from Database.database import *
from Database.schemas import *
from Models.model import *

import json


# Create tables
Base.metadata.create_all(bind=engine)

admin_router = APIRouter(
    tags=["Administrator"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------- Get запросы --------------------------------------------
@admin_router.get("/employee")
def get_employee(db: Session = Depends(get_db)):
    employees = db.query(EMPLOYEE).all()

    data = dict()
    data["employees"] = list()
    for e in employees:
        d = dict()
        d["employee_id"] = e.employee_id
        d["first_name"] = e.first_name
        d["last_name"] = e.last_name
        d["position"] = e.position
        data["employees"].append(d)

    return json.loads(json.dumps(data, default=str))


@admin_router.get("/room")
def get_room(db: Session = Depends(get_db)):
    room = db.query(ROOM).all()

    data = dict()
    data["room"] = list()
    for r in room:
        d = dict()
        d["room_id"] = r.room_id
        d["room_type"] = r.room_type
        d["price"] = r.price
        d["availability"] = r.availability
        data["room"].append(d)

    return json.loads(json.dumps(data, default=str))


@admin_router.get("/reservation")
def get_reservation(db: Session = Depends(get_db)):
    reservation = db.query(RESERVATION).all()

    data = dict()
    data["reservation"] = list()
    for r in reservation:
        d = dict()
        d["reservation_id"] = r.reservation_id
        d["guest_id"] = r.guest_id
        d["room_id"] = r.room_id
        d["check_in_date"] = r.check_in_date
        d["check_out_date"] = r.check_out_date
        data["reservation"].append(d)

    return json.loads(json.dumps(data, default=str))


@admin_router.get("/guest")
def get_guest(db: Session = Depends(get_db)):
    guest = db.query(GUEST).all()

    data = dict()
    data["guest"] = list()
    for g in guest:
        d = dict()
        d["guest_id"] = g.guest_id
        d["first_name"] = g.first_name
        d["last_name"] = g.last_name
        d["phone"] = g.phone
        data["guest"].append(d)

    return json.loads(json.dumps(data, default=str))


@admin_router.get("/service")
def get_service(db: Session = Depends(get_db)):
    service = db.query(SERVICE).all()

    data = dict()
    data["service"] = list()
    for s in service:
        d = dict()
        d["service_id"] = s.service_id
        d["service_name"] = s.service_name
        d["price"] = s.price
        data["service"].append(d)

    return json.loads(json.dumps(data, default=str))


# -------------------------------------------- Post запросы --------------------------------------------
@admin_router.post("/employee")
def add_employee(
    employee_data: EmployeeModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки

    employee = EMPLOYEE(
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        position=employee_data.position
    )
    db.add(employee)
    db.commit()

    return {"Сообщение": "Работник успешно добавлен"}


@admin_router.post("/room")
def add_room(
    room_data: RoomModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки

    room = ROOM(
        room_type=room_data.room_type,
        price=room_data.price,
        availability=room_data.availability
    )
    db.add(room)
    db.commit()

    return {"Сообщение": "Комната успешно добавлена"}


@admin_router.post("/reservation")
def add_reservation(
    reservation_data: ReservationModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки

    reservation = RESERVATION(
        guest_id=reservation_data.guest_id,
        room_id=reservation_data.room_id,
        check_in_date=reservation_data.check_in_date,
        check_out_date=reservation_data.check_out_date
    )
    db.add(reservation)
    db.commit()

    return {"Сообщение": "Бронирование успешно добавлено"}


@admin_router.post("/guest")
def add_guest(
    guest_data: GuestModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки

    guest = GUEST(
        first_name=guest_data.first_name,
        last_name=guest_data.last_name,
        phone=guest_data.phone
    )
    db.add(guest)
    db.commit()

    return {"Сообщение": "Бронирование успешно добавлено"}


@admin_router.post("/service")
def get_service(
    service_data: ServiceModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки

    service = SERVICE(
        service_name=service_data.service_name,
        price=service_data.price
    )
    db.add(service)
    db.commit()

    return {"Сообщение": "Бронирование успешно добавлено"}


# -------------------------------------------- Put запросы --------------------------------------------
@admin_router.put("/employee")
def change_employee_data(
    employee_data: EmployeeModel,
    new_employee_data: EmployeeModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки employee_data

    employee = db.query(EMPLOYEE)\
                 .filter(EMPLOYEE.employee_id == employee_data.id)\
                 .first()
    if employee is None:
        return JSONResponse(status_code=404, content={"Сообщение": ""})

    # Добавить проверки new_employee_data

    employee.first_name = new_employee_data.first_name
    employee.last_name = new_employee_data.last_name
    employee.position = new_employee_data.position

    db.commit()
    return {"Сообщение": ""}


@admin_router.put("/room")
def change_room_data(
    room_data: RoomModel,
    new_room_data: RoomModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки employee_data

    room = db.query(ROOM)\
                 .filter(ROOM.room_id == room_data.id)\
                 .first()
    if room is None:
        return JSONResponse(status_code=404, content={"Сообщение": ""})

    # Добавить проверки new_employee_data

    room.first_name = new_room_data.first_name
    room.last_name = new_room_data.last_name
    room.position = new_room_data.position

    db.commit()
    return {"Сообщение": ""}


@admin_router.put("/reservation")
def change_reservation_data(
    reservation_data: ReservationModel,
    new_reservation_data: ReservationModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки employee_data

    reservation = db.query(RESERVATION)\
                 .filter(RESERVATION.reservation_id == reservation_data.id)\
                 .first()
    if reservation is None:
        return JSONResponse(status_code=404, content={"Сообщение": ""})

    # Добавить проверки new_employee_data

    reservation.first_name = new_reservation_data.first_name
    reservation.last_name = new_reservation_data.last_name
    reservation.position = new_reservation_data.position

    db.commit()
    return {"Сообщение": ""}


@admin_router.put("/guest")
def change_guest_data(
    guest_data: GuestModel,
    new_guest_data: GuestModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки employee_data

    guest = db.query(GUEST)\
                 .filter(GUEST.guest_id == guest_data.id)\
                 .first()
    if guest is None:
        return JSONResponse(status_code=404, content={"Сообщение": ""})

    # Добавить проверки new_employee_data

    guest.first_name = new_guest_data.first_name
    guest.last_name = new_guest_data.last_name
    guest.position = new_guest_data.position

    db.commit()
    return {"Сообщение": ""}


@admin_router.put("/service")
def change_guest_data(
    service_data: ServiceModel,
    new_service_data: ServiceModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки employee_data

    service = db.query(SERVICE)\
                 .filter(SERVICE.service_id == service_data.id)\
                 .first()
    if service is None:
        return JSONResponse(status_code=404, content={"Сообщение": ""})

    # Добавить проверки new_employee_data

    service.first_name = new_service_data.first_name
    service.last_name = new_service_data.last_name
    service.position = new_service_data.position

    db.commit()
    return {"Сообщение": ""}


# -------------------------------------------- Delete запросы --------------------------------------------
@admin_router.delete("/employee")
def delete_employee(
    employee_data: EmployeeModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки employee_data

    employee = db.query(EMPLOYEE)\
                 .filter(EMPLOYEE.employee_id == employee_data.id)\
                 .first()
    if employee is None:
        return JSONResponse(status_code=404, content={"Сообщение": ""})

    db.delete(employee)
    db.commit()

    return {"Сообщение": ""}


@admin_router.delete("/room")
def delete_room(
    room_data: RoomModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки employee_data

    room = db.query(ROOM) \
        .filter(ROOM.room_id == room_data.id) \
        .first()
    if room is None:
        return JSONResponse(status_code=404, content={"Сообщение": ""})

    db.delete(room)
    db.commit()

    return {"Сообщение": ""}


@admin_router.delete("/reservation")
def delete_reservation(
    reservation_data: ReservationModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки employee_data

    reservation = db.query(RESERVATION) \
        .filter(RESERVATION.room_id == reservation_data.id) \
        .first()
    if reservation is None:
        return JSONResponse(status_code=404, content={"Сообщение": ""})

    db.delete(reservation)
    db.commit()

    return {"Сообщение": ""}


@admin_router.delete("/guest")
def delete_guest(
    guest_data: ReservationModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки employee_data

    guest = db.query(GUEST) \
        .filter(GUEST.room_id == guest_data.id) \
        .first()
    if guest is None:
        return JSONResponse(status_code=404, content={"Сообщение": ""})

    db.delete(guest)
    db.commit()

    return {"Сообщение": ""}


@admin_router.delete("/service")
def delete_service(
    service_data: ReservationModel,
    db: Session = Depends(get_db)
):
    # Добавить проверки employee_data

    service = db.query(SERVICE) \
        .filter(SERVICE.service_id == service_data.id) \
        .first()
    if service is None:
        return JSONResponse(status_code=404, content={"Сообщение": ""})

    db.delete(service)
    db.commit()

    return {"Сообщение": ""}
