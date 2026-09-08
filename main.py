from fastapi import FastAPI, Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import hashlib
import os

from database import Base, engine, get_db
from models import Employee

app = FastAPI(title="MindWell API")

# Create database tables
Base.metadata.create_all(bind=engine)


# -------------------------
# Password helper functions
# -------------------------

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


# -------------------------
# Request models
# -------------------------

class EmployeeCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "employee"


class LoginRequest(BaseModel):
    email: str
    password: str
    role: str


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return {
        "message": "MindWell API is running!"
    }


# -------------------------
# Health check
# -------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# -------------------------
# Create employee
# -------------------------

@app.post("/employees")
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
):

    existing_employee = db.query(Employee).filter(
        Employee.email == employee_data.email
    ).first()

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    employee = Employee(
        name=employee_data.name,
        email=employee_data.email,
        password_hash=hash_password(employee_data.password),
        role=employee_data.role
    )

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


# -------------------------
# Login
# -------------------------

@app.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    employee = db.query(Employee).filter(
        Employee.email == login_data.email
    ).first()

    if not employee:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if employee.role != login_data.role:
        raise HTTPException(
            status_code=401,
            detail="Invalid role"
        )

    if not verify_password(
        login_data.password,
        employee.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "employee_id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "role": employee.role
    }


# -------------------------
# Get all employees
# -------------------------

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