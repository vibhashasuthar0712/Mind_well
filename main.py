from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from risk_engine import calculate_risk

import hashlib
import json
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

    metrics: dict | None = None


# =========================================================
# MAIN HTML PAGES
# =========================================================


# LOGIN PAGE
@app.get("/")
def home():

    return FileResponse("index.html")


# EMPLOYEE DASHBOARD
@app.get("/employee")
def employee_page():

    return FileResponse("employee.html")


# RESPONDER DASHBOARD
@app.get("/responder")
def responder_page():

    return FileResponse("responder.html")


# HR DASHBOARD
@app.get("/hr")
def hr_page():

    return FileResponse("hr.html")


# =========================================================
# GAME PAGES
# =========================================================


# FOCUS HUNT
@app.get("/game")
def focus_game():

    return FileResponse("game.html")


# REACTION RUSH
@app.get("/reaction")
def reaction_game():

    return FileResponse("reaction.html")


# MEMORY MATCH
@app.get("/memory")
def memory_game():

    return FileResponse("memory.html")


# COLOR FLOW
@app.get("/color")
def color_game():

    return FileResponse("color.html")


# CHOICE QUEST
@app.get("/choice")
def choice_game():

    return FileResponse("choice.html")


# RELAX & RESET
@app.get("/relax")
def relax_page():

    return FileResponse("relax.html")


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

    # Normalize email
    email = employee_data.email.strip().lower()

    # Check if email already exists
    existing_employee = db.query(Employee).filter(
        Employee.email == email
    ).first()

    if existing_employee:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create employee
    employee = Employee(

        name=employee_data.name.strip(),

        email=email,

        password_hash=hash_password(
            employee_data.password
        ),

        role=employee_data.role.strip().lower()

    )

    # Save employee
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

    # Normalize input
    email = login_data.email.strip().lower()

    role = login_data.role.strip().lower()


    # Find employee
    employee = db.query(Employee).filter(
        Employee.email == email
    ).first()


    # Employee not found
    if not employee:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    # Check role
    if employee.role.strip().lower() != role:

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


    # Successful login
    return {

        "message": "Login successful",

        "employee_id": employee.id,

        "name": employee.name,

        "email": employee.email,

        "role": employee.role

    }


# =========================================================
# SAVE GAME RESULT
# =========================================================

@app.post("/game-results")
def save_game_result(
    result: GameResultCreate,
    db: Session = Depends(get_db)
):

    # Check employee exists
    employee = db.query(Employee).filter(
        Employee.id == result.employee_id
    ).first()


    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )


    # Create game result
    game_result = GameResult(

        employee_id=result.employee_id,

        game_name=result.game_name,

        time_taken=result.time_taken,

        correct=result.correct,

        wrong=result.wrong,

        accuracy=result.accuracy,

        score=result.score,

        metrics=json.dumps(result.metrics)
        if result.metrics
        else None

    )


    # Save result
    db.add(game_result)

    db.commit()

    db.refresh(game_result)


    return {

        "message": "Game result saved successfully",

        "result_id": game_result.id

    }


# =========================================================
# GET GAME RESULTS FOR EMPLOYEE
# =========================================================

@app.get("/game-results/{employee_id}")
def get_game_results(
    employee_id: int,
    db: Session = Depends(get_db)
):

    # Check employee exists
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()


    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )


    # Get results
    results = db.query(GameResult).filter(
        GameResult.employee_id == employee_id
    ).order_by(
        GameResult.created_at.asc()
    ).all()


    return [

        {

            "id": result.id,

            "game_name": result.game_name,

            "time_taken": result.time_taken,

            "correct": result.correct,

            "wrong": result.wrong,

            "accuracy": result.accuracy,

            "score": result.score,

            "metrics":
                json.loads(result.metrics)
                if result.metrics
                else {},

            "created_at": result.created_at

        }

        for result in results

    ]


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

@app.get("/risk/{employee_id}")
def get_employee_risk(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    results = db.query(GameResult).filter(
        GameResult.employee_id == employee_id
    ).order_by(
        GameResult.created_at.asc()
    ).all()

    risk = calculate_risk(results)

    return {
        "employee_id": employee_id,
        "employee_name": employee.name,
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "signals": risk["signals"],
        "message": risk["message"]
    }