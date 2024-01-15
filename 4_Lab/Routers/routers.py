from fastapi import APIRouter
from fastapi.responses import JSONResponse

from Database.database import *
from Shemas.shemas import *
from Models.models import UserModel

import re


Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.get("/")
def get_todo_list():
    db = SessionLocal()
    result = db.query(ToDo).all()
    db.close()
    return result


@router.post("/add")
def add_users(user_data: UserModel):
    db = SessionLocal()

    user = ToDo(
        name=user_data.name,
        task=user_data.task
    )
    db.add(user)
    db.commit()

    db.close()
    return {"message": "Пользователь успешно добавлен"}


@router.delete("/delete")
def del_users(user_data: UserModel, id: int):
    db = SessionLocal()
    user = db.query(ToDo)\
             .filter(ToDo.id == id)\
             .first()
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользоватеь не найден"})

    if user_data.name != user.name and user_data.task != user.task:
        return JSONResponse(status_code=404, content={"message": "Данные не верны"})

    db.delete(user)
    db.commit()

    db.close()
    return {"message": "Пользователь успешно удален"}


@router.put("/put")
def put_user(user_info: UserModel, id: int, name: str, task: str):
    db = SessionLocal()
    user = db.query(ToDo) \
        .filter(ToDo.id == id) \
        .first()
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользоватеь не найден"})

    if user_info.name != user.name and user_info.task != user.task:
        return JSONResponse(status_code=404, content={"message": "Данные не верны"})

    res = re.search(r"[A-Za-zА-Яа-я]", name)
    if res is not None:
        user.name = name
    else:
        return JSONResponse(status_code=404, content={"message": "Данные не верны"})
    res = re.search(r"[A-Za-zА-Яа-я]", task)
    if res is not None:
        user.task = task
    else:
        return JSONResponse(status_code=404, content={"message": "Данные не верны"})

    db.commit()
    db.close()
    return {"message": "Данные изменены"}

