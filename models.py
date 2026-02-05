from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Employee(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    puesto: str
    salario: float
    fecha_ingreso: datetime


class EmployeeInDB(Employee):
    id: str

class EmployeeCreate(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    puesto: str
    salario: float
    fecha_ingreso:  datetime


class EmployeeUpdate(BaseModel):
    nombre: Optional[str]
    apellido: Optional[str]
    email: Optional[EmailStr]
    puesto: Optional[str]
    salario: Optional[float]
    fecha_ingreso: Optional[datetime]
