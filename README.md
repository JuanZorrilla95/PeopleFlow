API interna para la gestión de empleados de PeopleFlow, desarrollada como challenge técnico backend.
Permite crear, consultar, actualizar y eliminar empleados, además de generar un reporte con el promedio de salarios solicitado por el área financiera.

Tecnologías utilizadas:
Python 3.10+
FastAPI
MongoDB
Pydantic
Uvicorn

Cómo levantar el proyecto:
1. Clonar el repositorio
    git clone <repo-url>
    cd PeopleFlow

2. python -m venv myenv
Linux/Mac: source myenv/bin/activate
Windows: myenv\Scripts\activate         

3. dependencias:
pip install -r requirements.txt

4. Levantar MongoDB
Asegurarse de que MongoDB esté corriendo en: mongodb://localhost:27017

5. ejecutar API
uvicorn main:app --reload
la api corre en http://127.0.0.1:8000

Documentacion Swagger: http://127.0.0.1:8000/docs

Endpoints disponibles:
Crear empleado: POST /employees

Listar empleados (filtros y paginado): GET /employees?puesto=Backend&page=1&limit=10

Obtener empleado por ID: GET /employees/{id}

Actualizar empleado: PUT /employees/{id}

Eliminar empleado: DELETE /employees/{id}

Promedio de salarios: GET /employees/average-salary


Decisiones técnicas:
- Se utiliza MongoDB como base NoSQL por su flexibilidad y rapidez para prototipos.
- El cálculo del promedio de salarios se hace mediante aggregations en MongoDB, evitando cargar datos innecesarios en memoria.
- Se normaliza fecha_ingreso a datetime antes de persistir, ya que MongoDB no admite date.
- Se valida unicidad de email a nivel de aplicación

Posibles mejoras (fuera de alcance del challenge):
- Autenticación (JWT)
- Tests automatizados
- Dockerización
- Índices en MongoDB
- Validación de reglas de negocio avanzadas

Autor: Juan Zorrilla Menez (juanzdev)
Backend / Full-Stack Developer
