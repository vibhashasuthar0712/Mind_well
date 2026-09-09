from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

import hashlib
import json
import os

from database import Base, engine, get_db
from models import Employee, GameResult, RiskCase
from risk_engine import calculate_risk


app = FastAPI(title="MindWell API")

Base.metadata.create_all(bind=engine)


# =====================================================
# PASSWORD FUNCTIONS
# =====================================================

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


# =====================================================
# PYDANTIC MODELS
# =====================================================

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


class StatusUpdate(BaseModel):

    status: str
    responder_notes: str | None = None


# =====================================================
# BASIC PAGES
# =====================================================

@app.get("/")
def home():

    return FileResponse("index.html")


@app.get("/employee")
def employee_page():

    return FileResponse("employee.html")


@app.get("/responder")
def responder_page():

    return FileResponse("responder.html")


@app.get("/hr")
def hr_page():

    return FileResponse("hr.html")


# =====================================================
# GAME PAGES
# =====================================================

@app.get("/game")
def focus_game():

    return FileResponse("game.html")


@app.get("/reaction")
def reaction_game():

    return FileResponse("reaction.html")


@app.get("/memory")
def memory_game():

    return FileResponse("memory.html")


@app.get("/color")
def color_game():

    return FileResponse("color.html")


@app.get("/choice")
def choice_game():

    return FileResponse("choice.html")


@app.get("/relax")
def relax_page():

    return FileResponse("relax.html")


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# =====================================================
# EMPLOYEE REGISTRATION
# =====================================================

@app.post("/employees")
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db)
):

    email = employee_data.email.strip().lower()

    existing_employee = db.query(Employee).filter(
        Employee.email == email
    ).first()

    if existing_employee:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    employee = Employee(
        name=employee_data.name.strip(),
        email=email,
        password_hash=hash_password(
            employee_data.password
        ),
        role=employee_data.role.strip().lower()
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


# =====================================================
# LOGIN
# =====================================================

@app.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):

    email = login_data.email.strip().lower()

    role = login_data.role.strip().lower()

    employee = db.query(Employee).filter(
        Employee.email == email
    ).first()

    if not employee:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if employee.role.strip().lower() != role:

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


# =====================================================
# SAVE GAME RESULT
# =====================================================

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

        score=result.score,

        metrics=json.dumps(result.metrics)
        if result.metrics
        else None
    )

    db.add(game_result)

    db.commit()

    db.refresh(game_result)


    # -------------------------------------------------
    # Calculate latest risk after every activity
    # -------------------------------------------------

    all_results = db.query(GameResult).filter(
        GameResult.employee_id == result.employee_id
    ).order_by(
        GameResult.created_at.asc()
    ).all()

    risk = calculate_risk(all_results)


    # -------------------------------------------------
    # Automatically create case for HIGH / CRITICAL
    # -------------------------------------------------

    if risk["risk_level"] in ["high", "critical"]:

        existing_case = db.query(RiskCase).filter(
            RiskCase.employee_id == result.employee_id,
            RiskCase.status.in_([
                "new",
                "acknowledged",
                "in_progress"
            ])
        ).first()

        # Don't create duplicate active cases
        if not existing_case:

            new_case = RiskCase(

                employee_id=result.employee_id,

                risk_score=risk["risk_score"],

                risk_level=risk["risk_level"],

                signals=json.dumps(
                    risk["signals"]
                ),

                status="new"
            )

            db.add(new_case)

            db.commit()


    return {

        "message": "Game result saved successfully",

        "result_id": game_result.id,

        "risk_score": risk["risk_score"],

        "risk_level": risk["risk_level"]
    }


# =====================================================
# GET EMPLOYEE GAME HISTORY
# =====================================================

@app.get("/game-results/{employee_id}")
def get_game_results(
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


# =====================================================
# GET ALL EMPLOYEES
# =====================================================

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


# =====================================================
# EMPLOYEE RISK
# =====================================================

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


# =====================================================
# RESPONDER DASHBOARD
# GET ACTIVE RISK CASES
# =====================================================

@app.get("/responder/cases")
def get_responder_cases(
    db: Session = Depends(get_db)
):

    cases = db.query(RiskCase).filter(
        RiskCase.status.in_([
            "new",
            "acknowledged",
            "in_progress"
        ])
    ).order_by(
        RiskCase.risk_score.desc(),
        RiskCase.created_at.desc()
    ).all()


    response = []


    for case in cases:

        employee = db.query(Employee).filter(
            Employee.id == case.employee_id
        ).first()


        response.append({

            "case_id": case.id,

            "employee_id": case.employee_id,

            "employee_name":
                employee.name
                if employee
                else "Unknown",

            "risk_score": case.risk_score,

            "risk_level": case.risk_level,

            "signals":
                json.loads(case.signals)
                if case.signals
                else [],

            "status": case.status,

            "responder_id": case.responder_id,

            "responder_notes":
                case.responder_notes,

            "created_at": case.created_at,

            "acknowledged_at":
                case.acknowledged_at
        })


    return response


# =====================================================
# ACKNOWLEDGE CASE
# =====================================================

@app.post("/responder/cases/{case_id}/acknowledge")
def acknowledge_case(
    case_id: int,
    db: Session = Depends(get_db)
):

    case = db.query(RiskCase).filter(
        RiskCase.id == case_id
    ).first()

    if not case:

        raise HTTPException(
            status_code=404,
            detail="Risk case not found"
        )


    if case.status != "new":

        return {

            "message": "Case is already acknowledged",

            "case_id": case.id,

            "status": case.status
        }


    case.status = "acknowledged"

    case.acknowledged_at = __import__(
        "datetime"
    ).datetime.utcnow()


    db.commit()

    db.refresh(case)


    return {

        "message": "Case acknowledged successfully",

        "case_id": case.id,

        "status": case.status
    }


# =====================================================
# UPDATE CASE STATUS
# =====================================================

@app.post("/responder/cases/{case_id}/status")
def update_case_status(
    case_id: int,
    status_data: StatusUpdate,
    db: Session = Depends(get_db)
):

    case = db.query(RiskCase).filter(
        RiskCase.id == case_id
    ).first()

    if not case:

        raise HTTPException(
            status_code=404,
            detail="Risk case not found"
        )


    allowed_statuses = [

        "new",

        "acknowledged",

        "in_progress",

        "resolved"
    ]


    new_status = status_data.status.strip().lower()


    if new_status not in allowed_statuses:

        raise HTTPException(

            status_code=400,

            detail=(
                "Invalid status. Use: "
                "new, acknowledged, "
                "in_progress, or resolved."
            )
        )


    case.status = new_status


    if status_data.responder_notes is not None:

        case.responder_notes = (
            status_data.responder_notes
        )


    if new_status == "resolved":

        case.resolved_at = __import__(
            "datetime"
        ).datetime.utcnow()


    db.commit()

    db.refresh(case)


    return {

        "message": "Case status updated",

        "case_id": case.id,

        "status": case.status,

        "responder_notes":
            case.responder_notes
    }