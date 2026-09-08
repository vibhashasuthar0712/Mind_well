from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
import hashlib
import os

from database import Base, engine, get_db
from models import Employee, GameResult


# =========================================================
# APP
# =========================================================

app = FastAPI(title="MindWell API")


# =========================================================
# DATABASE
# =========================================================

Base.metadata.create_all(bind=engine)


# =========================================================
# PASSWORD HELPER FUNCTIONS
# =========================================================

def hash_password(password: str, salt: str = None):

    if salt is None:
        salt = os.urandom(16).hex()

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    return f"{salt}:{password_hash}"


def verify_password(password: str, stored_hash: str):

    try:

        salt, saved_hash = stored_hash.split(":")

        new_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            100000
        ).hex()

        return new_hash == saved_hash

    except ValueError:

        return False


# =========================================================
# REQUEST MODELS
# =========================================================

class EmployeeCreate(BaseModel):

    name: str
    email: str
    password: str
    role: str = "employee"


class LoginRequest(BaseModel):

    email: str
    password: str
    role: str


class GameResultCreate(BaseModel):
    employee_id: int
    game_name: str
    time_taken: int | None = None
    correct: int | None = None
    wrong: int | None = None
    accuracy: int | None = None
    score: int | None = None


# =========================================================
# HTML PAGES
# =========================================================

# Login page
@app.get("/")
def home():

    return FileResponse("index.html")


# Employee dashboard
@app.get("/employee")
def employee_page():

    return FileResponse("employee.html")


# Responder dashboard
@app.get("/responder")
def responder_page():

    return FileResponse("responder.html")


# HR dashboard
@app.get("/hr")
def hr_page():

    return FileResponse("hr.html")


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# =========================================================
# CREATE EMPLOYEE
# =========================================================

@app.post("/employees")
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
):

    # Check if email already exists
    existing_employee = db.query(Employee).filter(
        Employee.email == employee_data.email
    ).first()

    if existing_employee:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create new employee
    employee = Employee(

        name=employee_data.name,

        email=employee_data.email,

        password_hash=hash_password(
            employee_data.password
        ),

        role=employee_data.role

    )

    # Save to database
    db.add(employee)

    db.commit()

    db.refresh(employee)

    return {

        "message": "Employee created successfully",

        "employee_id": employee.id,

        "name": employee.name,

        "email": employee.email,

        "role": employee.role

    }


# =========================================================
# LOGIN
# =========================================================

@app.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    # Find employee by email
    employee = db.query(Employee).filter(
        Employee.email == login_data.email
    ).first()

    # Email doesn't exist
    if not employee:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check role
    if employee.role != login_data.role:

        raise HTTPException(
            status_code=401,
            detail="Invalid role"
        )

    # Check password
    if not verify_password(
        login_data.password,
        employee.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Login successful
    return {

        "message": "Login successful",

        "employee_id": employee.id,

        "name": employee.name,

        "email": employee.email,

        "role": employee.role

    }


@app.post("/game-results")
def save_game_result(
    result: GameResultCreate,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.id == result.employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    game_result = GameResult(
        employee_id=result.employee_id,
        game_name=result.game_name,
        time_taken=result.time_taken,
        correct=result.correct,
        wrong=result.wrong,
        accuracy=result.accuracy,
        score=result.score
    )

    db.add(game_result)
    db.commit()
    db.refresh(game_result)

    return {
        "message": "Game result saved successfully",
        "result_id": game_result.id
    }


# =========================================================
# GET ALL EMPLOYEES
# =========================================================

@app.get("/employees")
def get_employees(
    db: Session = Depends(get_db)
):

    employees = db.query(Employee).all()

    return [

        {

            "id": employee.id,

            "name": employee.name,

            "email": employee.email,

            "role": employee.role,

            "created_at": employee.created_at

        }

        for employee in employees

    ]