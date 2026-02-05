from fastapi import FastAPI, HTTPException, Query, status
from bson import ObjectId
from bson.errors import InvalidId
from typing import List, Optional
from database import employees_collection
from models import EmployeeCreate, EmployeeInDB, Employee
from datetime import datetime 

app = FastAPI(title="PeopleFlow API")
@app.get("/")
def root():
    return {"status": "ok"}

def employee_helper(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "nombre": employee["nombre"],
        "apellido": employee["apellido"],
        "email": employee["email"],
        "puesto": employee["puesto"],
        "salario": employee["salario"],
        "fecha_ingreso": employee["fecha_ingreso"],
    }



@app.post("/employees", status_code=201)
def create_employee(employee: EmployeeCreate):
    # Validar email único
    existing = employees_collection.find_one({"email": employee.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")

    result = employees_collection.insert_one(employee.dict())
    new_employee = employees_collection.find_one({"_id": result.inserted_id})

    return employee_helper(new_employee)

#helper para convertir a mongo
def employee_serializer(employee) -> dict:
    return {
        "id": str(employee["_id"]),
        "nombre": employee["nombre"],
        "apellido": employee["apellido"],
        "email": employee["email"],
        "puesto": employee["puesto"],
        "salario": employee["salario"],
        "fecha_ingreso": employee["fecha_ingreso"],
    }

@app.get("/employees", response_model=List[EmployeeInDB])
def list_employees(
    puesto: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    skip = (page - 1) * limit

    query = {}
    if puesto:
        query["puesto"] = puesto

    employees = employees_collection.find(query).skip(skip).limit(limit)

    return [employee_serializer(emp) for emp in employees]


#endopoint para el promedio de los salarios
@app.get("/employees/average-salary")
def average_salary():
    pipeline = [
        {
            "$group": {
                "_id": None,
                "average_salary": {"$avg": "$salario"}
            }
        }
    ]

    result = list(employees_collection.aggregate(pipeline))

    if not result:
        return {"average_salary": 0}

    return {
        "average_salary": round(result[0]["average_salary"], 2)
    }

@app.get("/employees/{employee_id}", response_model=EmployeeInDB)
def get_employee(employee_id: str):
    try:
        employee = employees_collection.find_one(
            {"_id": ObjectId(employee_id)}
        )
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    if not employee:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    return employee_serializer(employee)

@app.post("/employees", response_model=EmployeeInDB, status_code=status.HTTP_201_CREATED)
def create_employee_with_id(employee: Employee):
    # validar email único
    if employees_collection.find_one({"email": employee.email}):
        raise HTTPException(
            status_code=400,
            detail="Email ya registrado"
        )

    employee_dict = employee.dict()
    employee_dict["fecha_ingreso"] = datetime.combine(
        employee.fecha_ingreso,
        datetime.min.time()
    )
    
    result = employees_collection.insert_one(employee_dict)

    created_employee = employees_collection.find_one(
        {"_id": result.inserted_id}
    )
    

    return employee_serializer(created_employee)

#endopoint para actualizar un empleado
@app.put("/employees/{employee_id}", response_model=EmployeeInDB)
def update_employee(employee_id: str, employee: Employee):
    try:
        obj_id = ObjectId(employee_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de empleado inválido")

    if not employees_collection.find_one({"_id": obj_id}):
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    employee_dict = employee.dict()
    employee_dict["fecha_ingreso"] = datetime.combine(
        employee.fecha_ingreso,
        datetime.min.time()
    )

    employees_collection.update_one(
        {"_id": obj_id},
        {"$set": employee_dict}
    )

    updated_employee = employees_collection.find_one({"_id": obj_id})
    return employee_serializer(updated_employee)

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):
    try:
        obj_id = ObjectId(employee_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de empleado inválido")

    result = employees_collection.delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    return {"message": "Empleado eliminado exitosamente"}