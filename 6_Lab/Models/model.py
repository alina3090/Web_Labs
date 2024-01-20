from pydantic import BaseModel, Field


class EmployeeModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    position: str


class RoomModel(BaseModel):
    id: int
    room_type: str
    price: int
    availability: bool


class ReservationModel(BaseModel):
    id: int
    guest_id: int
    room_id: int
    check_in_date: str
    check_out_date: str


class GuestModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str


class ServiceModel(BaseModel):
    # id: int
    service_name: str
    price: int
