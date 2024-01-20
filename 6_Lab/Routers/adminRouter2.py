# тут админ работает с услугами и работниками

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

admin_router2 = APIRouter(
    tags=["Administrator2"]
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

@admin_router2.get("/employee")
def get_employee(db: Session = Depends(get_db), role=Depends(KeycloakJWTBearerHandler())):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
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


@admin_router2.get("/service")
def get_service(db: Session = Depends(get_db), role=Depends(KeycloakJWTBearerHandler())):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
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


# -------------------------------------------- Post запросы на добавление--------------------------------------------
@admin_router2.post("/employee")
def add_employee(
        employee_data: EmployeeModel,
        db: Session = Depends(get_db),
        role=Depends(KeycloakJWTBearerHandler())
):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    # Добавить проверки
    if employee_data.first_name == '' or employee_data.last_name == '' or employee_data.position == '':
        return {"Сообщение": "Данные не введены"}
    employee = EMPLOYEE(
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        position=employee_data.position
    )
    db.add(employee)
    db.commit()

    return {"Сообщение": "Работник успешно добавлен"}


@admin_router2.post("/service")
def get_service(
        service_data: ServiceModel,
        db: Session = Depends(get_db),
        role=Depends(KeycloakJWTBearerHandler())
):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    # Добавить проверки
    if service_data.service_name == '' or service_data.price == '':
        return {"Сообщение": "Данные не введены"}
    service = SERVICE(
        service_name=service_data.service_name,
        price=service_data.price
    )
    db.add(service)
    db.commit()

    return {"Сообщение": "Услуга успешно добавлена"}


# -------------------------------------------- Put запросы --------------------------------------------
@admin_router2.put("/employee")
def change_employee_data(
        employee_data: EmployeeModel,
        new_employee_data: EmployeeModel,
        db: Session = Depends(get_db),
        role=Depends(KeycloakJWTBearerHandler())
):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    # Добавить проверки employee_data

    employee = db.query(EMPLOYEE) \
        .filter((EMPLOYEE.last_name == employee_data.last_name) &
                (EMPLOYEE.first_name == employee_data.first_name)
        )\
        .first()
    if employee is None:
        return JSONResponse(status_code=404, content={"Сообщение": "Работник не найден"})

    if new_employee_data.first_name == '' or new_employee_data.last_name == '' or new_employee_data.position == '':
        return {"Сообщение": "Новые данные работника не введены"}
    employee.first_name = new_employee_data.first_name
    employee.last_name = new_employee_data.last_name
    employee.position = new_employee_data.position

    db.commit()
    return {"Сообщение": "Данные работника изменены"}


@admin_router2.put("/service")
def change_guest_data(
        service_data: ServiceModel,
        new_service_data: ServiceModel,
        db: Session = Depends(get_db),
        role=Depends(KeycloakJWTBearerHandler())
):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    # Добавить проверки employee_data

    service = db.query(SERVICE) \
        .filter(
        (SERVICE.service_name == service_data.service_name) &
        (SERVICE.price == service_data.price)
    )\
        .first()
    if service is None:
        return JSONResponse(status_code=404, content={"Сообщение": ""})

    if new_service_data.price < 0:
        return {"Сообщение: неверная цена"}

    service.first_name = new_service_data.first_name
    service.last_name = new_service_data.last_name
    service.position = new_service_data.position

    db.commit()
    return {"Сообщение": "Данные услуги изменены"}


# -------------------------------------------- Delete запросы --------------------------------------------
@admin_router2.delete("/employee")
def delete_employee(
        employee_data: EmployeeModel,
        db: Session = Depends(get_db),
        role=Depends(KeycloakJWTBearerHandler())
):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    employee = db.query(EMPLOYEE) \
        .filter(EMPLOYEE.employee_id == employee_data.id) \
        .first()
    if employee is None:
        return JSONResponse(status_code=404, content={"Сообщение": "Работник не найден"})

    db.delete(employee)
    db.commit()

    return {"Сообщение": "Работник успено уволен"}


@admin_router2.delete("/service")
def delete_service(
        service_data: ServiceModel,
        db: Session = Depends(get_db),
        role=Depends(KeycloakJWTBearerHandler())
):
    if not verify_admin(role):
        raise HTTPException(status_code=403, detail={"message": "Denied permission"})
    # Добавить проверки employee_data
    # тут если не ввести id
    if service_data.service_name == '' or service_data.price == None:
        return {"Сообщение": "Данные не введены"}
    service = db.query(SERVICE) \
                .filter(
                    (SERVICE.service_name == service_data.service_name) &
                    (SERVICE.price == service_data.price)
                ) \
                .first()
    if service is None:
        return JSONResponse(status_code=404, content={"Сообщение": "Услуга не найдена"})

    db.delete(service)
    db.commit()

    return {"Сообщение": "Услуга успешно удалена"}
