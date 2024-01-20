from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from Database.database import *
from Database.schemas import *
from Models.model import *
from authorization import KeycloakJWTBearerHandler, HTTPException

import json


# Create tables
Base.metadata.create_all(bind=engine)

admin_router = APIRouter(
    tags=["Administrator"]
)


def verify_admin(role) -> bool:
    if role == "admin":
        return True
    return False


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------- Get запросы --------------------------------------------
@admin_router.get("/room")
def get_room(db: Session = Depends(get_db), role=Depends(KeycloakJWTBearerHandler())):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

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
def get_reservation(db: Session = Depends(get_db), role=Depends(KeycloakJWTBearerHandler())):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
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
def get_guest(db: Session = Depends(get_db), role=Depends(KeycloakJWTBearerHandler())):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
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


# -------------------------------------------- Post запросы  добавление --------------------------------------------

@admin_router.post("/reservation")
def add_reservation(
    reservation_data: ReservationModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    #проверка времени
    if (datetime.strptime(reservation_data.check_in_date, '%Y-%m-%d')) >= \
            (datetime.strptime(reservation_data.check_out_date, '%Y-%m-%d')):
        return {"Сообщение: даты введены неверно"}

    # Поиск гостя
    guest = db.query(GUEST) \
              .filter(GUEST.guest_id == reservation_data.guest_id) \
              .first()
    if guest is None:
        return JSONResponse(status_code=404, content={"Сообщение": "Гость не найден"})
    # поиск комнаты
    # проерка занята ли комната?
    room = db.query(ROOM) \
             .filter(ROOM.room_id == reservation_data.room_id) \
             .first()
    if room is None:
        return JSONResponse(status_code=404, content={"Сообщение": "Комната не найдена"})
    elif room.availability == False:
        return {"Сообщение: комната занята"}
    else:
        room.availability = False

    reservation = RESERVATION(
        guest_id=reservation_data.guest_id,
        room_id=reservation_data.room_id,
        check_in_date=datetime.strptime(reservation_data.check_in_date, '%Y-%m-%d'),
        check_out_date=datetime.strptime(reservation_data.check_out_date, '%Y-%m-%d')
    )

    db.add(reservation)
    db.commit()

    return {"Сообщение": "Бронирование успешно добавлено"}


@admin_router.post("/guest")
def add_guest(
    guest_data: GuestModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    if guest_data.first_name == '' or guest_data.last_name =='' or guest_data.phone == '':
        return {"Сообщение": "Данные не введены"}

    guest = GUEST(
        first_name=guest_data.first_name,
        last_name=guest_data.last_name,
        phone=guest_data.phone
    )
    db.add(guest)
    db.commit()

    return {"Сообщение": "Гость успешно добавлен"}


# -------------------------------------------- Put запросы --------------------------------------------
@admin_router.put("/room")
def change_room_data(
    room_data: RoomModel,
    price: int,
    # new_room_data: RoomModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    # Добавить проверки employee_data

    room = db.query(ROOM)\
                 .filter(ROOM.room_id == room_data.id)\
                 .first()
    if room is None:
        return JSONResponse(status_code=404, content={"Сообщение": "Комната не найдена"})

    if price < 0:
        return{"Сообщение": "Данные не введены"}

    room.price = price

    db.commit()
    return {"Сообщение": "Данные изменены"}


@admin_router.put("/guest")
def change_guest_data(
    guest_data: GuestModel,
    new_guest_data: GuestModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    guest = (db.query(GUEST)\
                 .filter(
                    (GUEST.last_name == guest_data.last_name) &
                    (GUEST.first_name == guest_data.first_name) &
                    (GUEST.phone == guest_data.phone)
                )\
                 .first())
    if guest is None:
        return JSONResponse(status_code=404, content={"Сообщение": "Гость не найден"})

    if new_guest_data.first_name == '' or new_guest_data.last_name == '' or new_guest_data.phone == '':
        return {"Сообщение": "Новые данные не введены"}

    guest.first_name = new_guest_data.first_name
    guest.last_name = new_guest_data.last_name
    guest.position = new_guest_data.phone

    db.commit()
    return {"Сообщение": "Данные гостя изменены"}


# -------------------------------------------- Delete запросы --------------------------------------------
@admin_router.delete("/guest")
def delete_guest(
    guest_data: GuestModel,
    db: Session = Depends(get_db),
    role=Depends(KeycloakJWTBearerHandler())
):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})

    if guest_data.first_name == '' or guest_data.last_name == '' or guest_data.phone == '':
        return {"Сообщение": "Данные не введены"}
    guest = db.query(GUEST) \
        .filter(GUEST.room_id == guest_data.id) \
        .first()
    if guest is None:
        return JSONResponse(status_code=404, content={"Сообщение": "Гость не найден"})

    db.delete(guest)
    db.commit()

    return {"Сообщение": "Гость удален"}

