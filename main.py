import os
import json
import hashlib
from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import engine, get_db, Base
from models import Employee, GameResult, RiskCase, JournalEntry
from risk_engine import calculate_risk


# ============================================================
# OPTIONAL OPENAI
# ============================================================

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(title="Wellora API")


# ============================================================
# OPTIONAL OPENAI CONFIGURATION
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OpenAI and OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None


# ============================================================
# REQUEST MODELS
# ============================================================

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "employee"


class LoginRequest(BaseModel):
    email: str
    password: str
    role: str


class GameResultRequest(BaseModel):
    employee_id: int
    game_name: str
    time_taken: int | None = None
    correct: int | None = None
    wrong: int | None = None
    accuracy: int | None = None
    score: int | None = None
    metrics: dict | None = None


class StatusUpdateRequest(BaseModel):
    status: str


class EscalationRequest(BaseModel):
    employee_contacted: bool = False
    support_required: bool = False
    escalation_level: str = "secondary_responder"
    escalation_reason: str | None = None


class CheckinRequest(BaseModel):
    employee_contacted: bool = False
    support_required: bool = False
    checkin_notes: str = ""
    outcome: str = "continue_support"


class TalkRequest(BaseModel):
    employee_id: int | None = None
    message: str


# ============================================================
# PRIVATE JOURNAL REQUEST MODEL
# ============================================================

class JournalEntryRequest(BaseModel):
    employee_id: int
    content: str
    feeling_after: str | None = None


# ============================================================
# PASSWORD HELPERS
# ============================================================

def hash_password(password: str):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def verify_password(password: str, password_hash: str):
    return hash_password(password) == password_hash


# ============================================================
# BASIC ROUTE
# ============================================================

@app.get("/")
def home():

    try:

        with open(
            "index.html",
            "r",
            encoding="utf-8"
        ) as file:

            return HTMLResponse(
                file.read()
            )

    except FileNotFoundError:

        return {
            "message": "Wellora API is running."
        }


# ============================================================
# PAGE ROUTES
# ============================================================

@app.get("/employee", response_class=HTMLResponse)
def employee_page():

    with open(
        "employee.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(
            file.read()
        )


@app.get("/checkin", response_class=HTMLResponse)
def checkin_page():

    with open(
        "checkin.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(
            file.read()
        )


@app.get("/hr", response_class=HTMLResponse)
def hr_page():

    with open(
        "hr.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(
            file.read()
        )


@app.get("/responder", response_class=HTMLResponse)
def responder_page():

    with open(
        "responder.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(
            file.read()
        )


@app.get("/game", response_class=HTMLResponse)
def game_page():

    with open(
        "game.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(
            file.read()
        )


@app.get("/reaction", response_class=HTMLResponse)
def reaction_page():

    with open(
        "reaction.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(
            file.read()
        )


@app.get("/memory", response_class=HTMLResponse)
def memory_page():

    with open(
        "memory.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(
            file.read()
        )


@app.get("/color", response_class=HTMLResponse)
def color_page():

    with open(
        "color.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(
            file.read()
        )


@app.get("/choice", response_class=HTMLResponse)
def choice_page():

    with open(
        "choice.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(
            file.read()
        )


@app.get("/relax", response_class=HTMLResponse)
def relax_page():

    with open(
        "relax.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(
            file.read()
        )


@app.get("/talk", response_class=HTMLResponse)
def talk_page():

    with open(
        "talk.html",
        "r",
        encoding="utf-8"
    ) as file:

        return HTMLResponse(
            file.read()
        )


# ============================================================
# PRIVATE JOURNAL PAGE
# ============================================================

@app.get("/journal", response_class=HTMLResponse)
def journal_page():

    try:

        with open(
            "journal.html",
            "r",
            encoding="utf-8"
        ) as file:

            return HTMLResponse(
                file.read()
            )

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="Journal page not found."
        )


# ============================================================
# REGISTER
# ============================================================

@app.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_employee = (
        db.query(Employee)
        .filter(
            Employee.email == request.email
        )
        .first()
    )

    if existing_employee:

        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    employee = Employee(
        name=request.name,
        email=request.email,
        password_hash=hash_password(
            request.password
        ),
        role=request.role
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return {
        "message": "Registration successful",
        "employee_id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "role": employee.role
    }


# ============================================================
# LOGIN
# ============================================================

@app.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    employee = (
        db.query(Employee)
        .filter(
            Employee.email == request.email
        )
        .first()
    )

    if not employee:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        request.password,
        employee.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    # --------------------------------------------------------
    # Check selected role
    # --------------------------------------------------------

    if employee.role != request.role:

        raise HTTPException(
            status_code=401,
            detail=(
                f"This account is registered as "
                f"{employee.role}. "
                f"Please select the correct role."
            )
        )

    return {
        "message": "Login successful",
        "employee_id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "role": employee.role
    }


# ============================================================
# SAVE GAME RESULT
# ============================================================

@app.post("/game-result")
def save_game_result(
    request: GameResultRequest,
    db: Session = Depends(get_db)
):

    employee = (
        db.query(Employee)
        .filter(
            Employee.id == request.employee_id
        )
        .first()
    )

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    result = GameResult(

        employee_id=request.employee_id,

        game_name=request.game_name,

        time_taken=request.time_taken,

        correct=request.correct,

        wrong=request.wrong,

        accuracy=request.accuracy,

        score=request.score,

        metrics=(
            json.dumps(request.metrics)
            if request.metrics
            else None
        )
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    # --------------------------------------------------------
    # Calculate current risk
    # --------------------------------------------------------

    all_results = (
        db.query(GameResult)
        .filter(
            GameResult.employee_id ==
            request.employee_id
        )
        .order_by(
            GameResult.created_at.asc()
        )
        .all()
    )

    risk = calculate_risk(
        all_results
    )

    # --------------------------------------------------------
    # Create RiskCase for high / critical
    # --------------------------------------------------------

    if risk["risk_level"] in [
        "high",
        "critical"
    ]:

        existing_case = (
            db.query(RiskCase)
            .filter(
                RiskCase.employee_id ==
                request.employee_id,

                RiskCase.status.in_(
                    [
                        "new",
                        "in_progress"
                    ]
                )
            )
            .first()
        )

        if not existing_case:

            risk_case = RiskCase(

                employee_id=request.employee_id,

                risk_score=risk["risk_score"],

                risk_level=risk["risk_level"],

                signals=json.dumps(
                    risk["signals"]
                ),

                status="new"
            )

            db.add(risk_case)
            db.commit()
            db.refresh(risk_case)

    return {

        "message":
            "Game result saved",

        "game_result_id":
            result.id,

        "risk_score":
            risk["risk_score"],

        "risk_level":
            risk["risk_level"],

        "signals":
            risk["signals"],

        "risk_message":
            risk["message"]
    }


# ============================================================
# GAME HISTORY
# ============================================================

@app.get("/game-history/{employee_id}")
def game_history(
    employee_id: int,
    db: Session = Depends(get_db)
):

    results = (
        db.query(GameResult)
        .filter(
            GameResult.employee_id ==
            employee_id
        )
        .order_by(
            GameResult.created_at.asc()
        )
        .all()
    )

    return [

        {
            "id":
                result.id,

            "game_name":
                result.game_name,

            "time_taken":
                result.time_taken,

            "correct":
                result.correct,

            "wrong":
                result.wrong,

            "accuracy":
                result.accuracy,

            "score":
                result.score,

            "metrics": (
                json.loads(result.metrics)
                if result.metrics
                else {}
            ),

            "created_at":
                result.created_at
        }

        for result in results
    ]


# ============================================================
# EMPLOYEE RISK
# ============================================================

@app.get("/employee-risk/{employee_id}")
def employee_risk(
    employee_id: int,
    db: Session = Depends(get_db)
):

    results = (
        db.query(GameResult)
        .filter(
            GameResult.employee_id ==
            employee_id
        )
        .order_by(
            GameResult.created_at.asc()
        )
        .all()
    )

    return calculate_risk(
        results
    )


# ============================================================
# EMPLOYEE LIST
# ============================================================

@app.get("/employees")
def employees(
    db: Session = Depends(get_db)
):

    employee_list = (
        db.query(Employee)
        .filter(
            Employee.role == "employee"
        )
        .all()
    )

    return [

        {
            "id":
                employee.id,

            "name":
                employee.name,

            "email":
                employee.email,

            "role":
                employee.role
        }

        for employee in employee_list
    ]


# ============================================================
# RESPONDER - ACTIVE CASES
# ============================================================

@app.get("/responder/cases")
def responder_cases(
    db: Session = Depends(get_db)
):

    cases = (
        db.query(RiskCase)
        .filter(
            RiskCase.status.in_(
                [
                    "new",
                    "in_progress"
                ]
            )
        )
        .order_by(
            RiskCase.created_at.desc()
        )
        .all()
    )

    response = []

    for case in cases:

        employee = (
            db.query(Employee)
            .filter(
                Employee.id ==
                case.employee_id
            )
            .first()
        )

        response.append(

            {
                "id":
                    case.id,

                "employee_id":
                    case.employee_id,

                "employee_name": (
                    employee.name
                    if employee
                    else "Unknown"
                ),

                "employee_email": (
                    employee.email
                    if employee
                    else ""
                ),

                "risk_score":
                    case.risk_score,

                "risk_level":
                    case.risk_level,

                "signals": (
                    json.loads(case.signals)
                    if case.signals
                    else []
                ),

                "status":
                    case.status,

                "responder_id":
                    case.responder_id,

                "responder_notes":
                    case.responder_notes,

                "escalation_level":
                    case.escalation_level,

                "escalation_reason":
                    case.escalation_reason,

                "escalated_at":
                    case.escalated_at,

                "employee_contacted":
                    bool(
                        case.employee_contacted
                    ),

                "support_required":
                    bool(
                        case.support_required
                    ),

                "created_at":
                    case.created_at,

                "acknowledged_at":
                    case.acknowledged_at,

                "resolved_at":
                    case.resolved_at
            }
        )

    return response


# ============================================================
# ACKNOWLEDGE CASE
# ============================================================

@app.post(
    "/responder/cases/{case_id}/acknowledge"
)
def acknowledge_case(
    case_id: int,
    db: Session = Depends(get_db)
):

    case = (
        db.query(RiskCase)
        .filter(
            RiskCase.id == case_id
        )
        .first()
    )

    if not case:

        raise HTTPException(
            status_code=404,
            detail="Risk case not found."
        )

    case.status = "in_progress"

    case.acknowledged_at = (
        datetime.utcnow()
    )

    db.commit()
    db.refresh(case)

    return {

        "message":
            "Case acknowledged",

        "case_id":
            case.id,

        "status":
            case.status,

        "acknowledged_at":
            case.acknowledged_at
    }


# ============================================================
# UPDATE CASE STATUS
# ============================================================

@app.post(
    "/responder/cases/{case_id}/status"
)
def update_case_status(
    case_id: int,
    request: StatusUpdateRequest,
    db: Session = Depends(get_db)
):

    allowed_statuses = [
        "new",
        "in_progress",
        "resolved"
    ]

    if request.status not in allowed_statuses:

        raise HTTPException(
            status_code=400,
            detail="Invalid case status."
        )

    case = (
        db.query(RiskCase)
        .filter(
            RiskCase.id == case_id
        )
        .first()
    )

    if not case:

        raise HTTPException(
            status_code=404,
            detail="Risk case not found."
        )

    case.status = request.status

    if request.status == "resolved":

        case.resolved_at = (
            datetime.utcnow()
        )

    db.commit()
    db.refresh(case)

    return {

        "message":
            "Case status updated",

        "case_id":
            case.id,

        "status":
            case.status
    }


# ============================================================
# ESCALATE CASE
# ============================================================

@app.post(
    "/responder/cases/{case_id}/escalate"
)
def escalate_case(
    case_id: int,
    request: EscalationRequest,
    db: Session = Depends(get_db)
):

    case = (
        db.query(RiskCase)
        .filter(
            RiskCase.id == case_id
        )
        .first()
    )

    if not case:

        raise HTTPException(
            status_code=404,
            detail="Risk case not found."
        )

    case.status = "in_progress"

    case.escalation_level = (
        request.escalation_level
    )

    case.escalation_reason = (
        request.escalation_reason
    )

    case.escalated_at = (
        datetime.utcnow()
    )

    case.employee_contacted = (
        1
        if request.employee_contacted
        else 0
    )

    case.support_required = (
        1
        if request.support_required
        else 0
    )

    db.commit()
    db.refresh(case)

    return {

        "message":
            "Safety escalation recorded",

        "case_id":
            case.id,

        "status":
            case.status,

        "escalation_level":
            case.escalation_level,

        "employee_contacted":
            bool(
                case.employee_contacted
            ),

        "support_required":
            bool(
                case.support_required
            ),

        "escalated_at":
            case.escalated_at
    }


# ============================================================
# HR OVERVIEW
# ============================================================

@app.get("/hr/overview")
def hr_overview(
    db: Session = Depends(get_db)
):

    employees = (
        db.query(Employee)
        .filter(
            Employee.role == "employee"
        )
        .all()
    )

    total_employees = len(
        employees
    )

    stable = 0
    elevated = 0
    high = 0
    critical = 0

    risk_scores = []

    for employee in employees:

        results = (
            db.query(GameResult)
            .filter(
                GameResult.employee_id ==
                employee.id
            )
            .order_by(
                GameResult.created_at.asc()
            )
            .all()
        )

        risk = calculate_risk(
            results
        )

        risk_level = risk[
            "risk_level"
        ]

        risk_score = risk[
            "risk_score"
        ]

        risk_scores.append(
            risk_score
        )

        if risk_level == "low":

            stable += 1

        elif risk_level == "elevated":

            elevated += 1

        elif risk_level == "high":

            high += 1

        elif risk_level == "critical":

            critical += 1

    average_risk_score = (

        round(
            sum(risk_scores)
            / len(risk_scores)
        )

        if risk_scores

        else 0
    )

    if critical > 0:

        organization_status = (
            "Action Required"
        )

    elif high > 0:

        organization_status = (
            "Needs Attention"
        )

    elif elevated > 0:

        organization_status = (
            "Monitor"
        )

    else:

        organization_status = (
            "Stable"
        )

    return {

        "organization_status":
            organization_status,

        "total_employees":
            total_employees,

        "stable":
            stable,

        "elevated":
            elevated,

        "high":
            high,

        "critical":
            critical,

        "average_risk_score":
            average_risk_score
    }


# ============================================================
# TALK & SHARE - SAFETY DETECTION
# ============================================================

def detect_safety_concern(
    message: str
):

    text = message.lower()

    safety_keywords = [

        "suicide",

        "kill myself",

        "end my life",

        "want to die",

        "don't want to live",

        "dont want to live",

        "hurt myself",

        "harm myself",

        "self harm",

        "self-harm",

        "take my life",

        "ending my life"
    ]

    for keyword in safety_keywords:

        if keyword in text:

            return True

    return False


# ============================================================
# TALK & SHARE - FALLBACK ASSISTANT
# ============================================================

def generate_fallback_reply(
    message: str
):

    """
    Context-aware Wellora assistant.

    Used when no OpenAI API key is available.

    This is supportive guidance only.
    It does not diagnose any mental-health condition.
    """

    text = (
        message
        .lower()
        .strip()
    )

    # --------------------------------------------------------
    # SAFETY
    # --------------------------------------------------------

    if detect_safety_concern(text):

        return {

            "reply": (
                "I'm really sorry you're going through "
                "something this difficult. You don't have "
                "to handle it alone. Please move to a safe "
                "place and reach out to a trusted person "
                "who can stay with you. If you may act on "
                "these thoughts or are in immediate danger, "
                "contact your local emergency service or "
                "an appropriate crisis service now."
            ),

            "safety_support":
                True,

            "safety_message": (
                "This may need immediate human support. "
                "Please contact a trusted person or "
                "appropriate emergency/crisis support."
            )
        }

    # --------------------------------------------------------
    # WORKLOAD
    # --------------------------------------------------------

    workload_words = [

        "workload",

        "too much work",

        "much work",

        "lots of work",

        "lot of work",

        "heavy workload",

        "overloaded",

        "overload",

        "work pressure",

        "pressure at work"
    ]

    if any(
        word in text
        for word in workload_words
    ):

        return {

            "reply": (
                "That sounds exhausting, especially when "
                "the workload keeps piling up. 💙\n\n"
                "Try breaking your workload into three "
                "groups: urgent, important, and can-wait. "
                "Start with the most urgent task instead "
                "of trying to handle everything at once.\n\n"
                "If there is more work than you can "
                "realistically finish, it may also help "
                "to tell your manager which tasks you can "
                "complete by the deadline and ask which "
                "ones should be prioritized."
            ),

            "safety_support":
                False,

            "safety_message":
                None
        }

    # --------------------------------------------------------
    # BOSS / MANAGER
    # --------------------------------------------------------

    boss_words = [

        "boss",

        "manager",

        "supervisor",

        "senior",

        "my lead",

        "team lead"
    ]

    if any(
        word in text
        for word in boss_words
    ):

        return {

            "reply": (
                "It sounds like the pressure may be coming "
                "from having more tasks than you can "
                "comfortably manage.\n\n"
                "One useful step is to have a short "
                "conversation with your manager about "
                "priorities rather than simply saying "
                "there is too much work.\n\n"
                "You can explain what you're currently "
                "working on, what the deadlines are, and "
                "ask which task should come first."
            ),

            "safety_support":
                False,

            "safety_message":
                None
        }

    # --------------------------------------------------------
    # DEADLINE
    # --------------------------------------------------------

    deadline_words = [

        "deadline",

        "before saturday",

        "by saturday",

        "due",

        "deadline pressure",

        "finish before",

        "complete before"
    ]

    if any(
        word in text
        for word in deadline_words
    ):

        return {

            "reply": (
                "A tight deadline can make everything feel "
                "much heavier. Try not to look at the entire "
                "workload at once.\n\n"
                "Write down the tasks that must be finished "
                "before the deadline, estimate how long each "
                "one will take, and start with the "
                "highest-priority item.\n\n"
                "If the total time is more than the time "
                "available, tell your manager early and ask "
                "them to help prioritize."
            ),

            "safety_support":
                False,

            "safety_message":
                None
        }

    # --------------------------------------------------------
    # TIRED / EXHAUSTED
    # --------------------------------------------------------

    tired_words = [

        "tired",

        "tiring",

        "exhausted",

        "exhausting",

        "drained",

        "no energy",

        "low energy",

        "can't keep up",

        "cannot keep up"
    ]

    if any(
        word in text
        for word in tired_words
    ):

        return {

            "reply": (
                "It sounds like you're feeling pretty "
                "drained. When work is demanding, even "
                "small things can start feeling difficult.\n\n"
                "If possible, take a short break, step away "
                "from the screen for a few minutes, get some "
                "water, and then return to one task at a "
                "time.\n\n"
                "You don't have to solve the entire workload "
                "in one go."
            ),

            "safety_support":
                False,

            "safety_message":
                None
        }

    # --------------------------------------------------------
    # FOCUS
    # --------------------------------------------------------

    focus_words = [

        "focus",

        "focusing",

        "concentrate",

        "concentration",

        "distracted",

        "can't concentrate",

        "cannot concentrate"
    ]

    if any(
        word in text
        for word in focus_words
    ):

        return {

            "reply": (
                "When your mind is overloaded, focusing can "
                "become much harder.\n\n"
                "Try choosing just one small task and "
                "working on it for 20–25 minutes without "
                "switching between tasks. After that, take "
                "a short break and decide what needs your "
                "attention next."
            ),

            "safety_support":
                False,

            "safety_message":
                None
        }

    # --------------------------------------------------------
    # STRESS / OVERWHELMED
    # --------------------------------------------------------

    stress_words = [

        "stress",

        "stressed",

        "overwhelmed",

        "anxious",

        "anxiety",

        "pressure",

        "frustrated",

        "frustrating"
    ]

    if any(
        word in text
        for word in stress_words
    ):

        return {

            "reply": (
                "It sounds like there is a lot on your mind "
                "right now. 💙\n\n"
                "Before trying to solve everything, take a "
                "moment to slow things down. Identify the "
                "one thing that needs attention first.\n\n"
                "If the pressure is mainly coming from work, "
                "it may also help to discuss priorities or "
                "deadlines with your manager."
            ),

            "safety_support":
                False,

            "safety_message":
                None
        }

    # --------------------------------------------------------
    # HELP / ADVICE
    # --------------------------------------------------------

    help_words = [

        "what can i do",

        "what should i do",

        "help me",

        "how can i",

        "what do i do",

        "suggest",

        "suggestion",

        "advice"
    ]

    if any(
        word in text
        for word in help_words
    ):

        return {

            "reply": (
                "Let's keep it simple. Start with the next "
                "small step rather than trying to fix "
                "everything at once.\n\n"
                "1. List what needs to be done.\n"
                "2. Mark the most urgent task.\n"
                "3. Work on that task without switching "
                "around.\n"
                "4. Take a short break after a focused "
                "work block.\n"
                "5. If the workload still doesn't fit the "
                "deadline, talk to your manager about "
                "priorities."
            ),

            "safety_support":
                False,

            "safety_message":
                None
        }

    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    greeting_words = [

        "hi",

        "hello",

        "hey",

        "hii",

        "good morning",

        "good evening",

        "good afternoon"
    ]

    if text in greeting_words:

        return {

            "reply": (
                "Hi! 💙 I'm here to listen. You can talk "
                "about work pressure, workload, focus, "
                "feeling overwhelmed, or simply how your "
                "day is going."
            ),

            "safety_support":
                False,

            "safety_message":
                None
        }

    # --------------------------------------------------------
    # GENERAL RESPONSE
    # --------------------------------------------------------

    return {

        "reply": (
            "Thanks for sharing that with me. 💙 "
            "It sounds like something is bothering you. "
            "If you'd like, tell me a little more about "
            "what has been difficult today, and we can "
            "break it down into something manageable."
        ),

        "safety_support":
            False,

        "safety_message":
            None
    }


# ============================================================
# TALK & SHARE ENDPOINT
# ============================================================

@app.post("/talk")
def talk(
    request: TalkRequest
):

    message = request.message.strip()

    if not message:

        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    if len(message) > 2000:

        raise HTTPException(
            status_code=400,
            detail="Message is too long."
        )

    # --------------------------------------------------------
    # Safety check first
    # --------------------------------------------------------

    if detect_safety_concern(
        message
    ):

        return generate_fallback_reply(
            message
        )

    # --------------------------------------------------------
    # OpenAI mode
    # --------------------------------------------------------

    if client is not None:

        try:

            system_prompt = """
You are Wellora's Talk & Share wellbeing assistant.

Your role is to provide supportive, empathetic and practical
conversation for workplace wellbeing.

Important rules:

1. Do not diagnose mental-health conditions.
2. Do not claim that a game or activity can diagnose stress,
   anxiety, depression or any other condition.
3. Treat Wellora activity data only as possible wellbeing signals.
4. Encourage practical steps such as breaks, prioritization,
   communication and appropriate human support.
5. Do not pretend that you contacted HR, a responder,
   family member, emergency services or anyone else.
6. If a user expresses possible immediate danger or self-harm,
   encourage immediate human/emergency support.
7. Keep responses conversational and reasonably short.
8. Respond directly to what the user actually said.
9. Avoid repeating generic responses.
10. For workplace workload issues, give practical suggestions.
"""

            response = client.responses.create(

                model="gpt-5.6-luna",

                instructions=system_prompt,

                input=message
            )

            reply = response.output_text

            return {

                "reply":
                    reply,

                "safety_support":
                    False,

                "safety_message":
                    None
            }

        except Exception as error:

            print(
                "OpenAI request failed:",
                str(error)
            )

            return generate_fallback_reply(
                message
            )

    # --------------------------------------------------------
    # No API key
    # --------------------------------------------------------

    return generate_fallback_reply(
        message
    )


# ============================================================
# PRIVATE JOURNAL - SAVE ENTRY
# ============================================================

@app.post("/journal")
def save_journal_entry(
    request: JournalEntryRequest,
    db: Session = Depends(get_db)
):

    content = request.content.strip()

    # --------------------------------------------------------
    # Validate content
    # --------------------------------------------------------

    if not content:

        raise HTTPException(
            status_code=400,
            detail="Journal entry cannot be empty."
        )

    if len(content) > 10000:

        raise HTTPException(
            status_code=400,
            detail="Journal entry is too long."
        )

    # --------------------------------------------------------
    # Validate optional feeling
    # --------------------------------------------------------

    allowed_feelings = [
        "A little better",
        "Same as before",
        "Still overwhelmed",
        "More calm",
        "Prefer not to say"
    ]

    feeling_after = request.feeling_after

    if feeling_after is not None:

        feeling_after = feeling_after.strip()

        if feeling_after == "":

            feeling_after = None

        elif feeling_after not in allowed_feelings:

            raise HTTPException(
                status_code=400,
                detail="Invalid feeling selection."
            )

    # --------------------------------------------------------
    # Verify employee exists
    # --------------------------------------------------------

    employee = (
        db.query(Employee)
        .filter(
            Employee.id == request.employee_id
        )
        .first()
    )

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    # --------------------------------------------------------
    # Create private journal entry
    #
    # IMPORTANT:
    # This is intentionally NOT connected to:
    # - calculate_risk()
    # - RiskCase
    # - HR
    # - Responder
    # - Talk & Share AI
    # --------------------------------------------------------

    entry = JournalEntry(

        employee_id=request.employee_id,

        content=content,

        feeling_after=feeling_after
    )

    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {

        "message":
            "Journal entry saved privately.",

        "entry_id":
            entry.id,

        "feeling_after":
            entry.feeling_after,

        "created_at":
            entry.created_at
    }


# ============================================================
# PRIVATE JOURNAL - GET ENTRIES
# ============================================================

@app.get("/journal/{employee_id}")
def get_journal_entries(
    employee_id: int,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # Verify employee exists
    # --------------------------------------------------------

    employee = (
        db.query(Employee)
        .filter(
            Employee.id == employee_id
        )
        .first()
    )

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    # --------------------------------------------------------
    # Get only this employee's journal entries
    # --------------------------------------------------------

    entries = (
        db.query(JournalEntry)
        .filter(
            JournalEntry.employee_id ==
            employee_id
        )
        .order_by(
            JournalEntry.created_at.desc()
        )
        .all()
    )

    return [

        {
            "id":
                entry.id,

            "content":
                entry.content,

            "feeling_after":
                entry.feeling_after,

            "created_at":
                entry.created_at
        }

        for entry in entries
    ]


# ============================================================
# PRIVATE JOURNAL - DELETE ENTRY
# ============================================================

@app.delete("/journal/{entry_id}")
def delete_journal_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):

    entry = (
        db.query(JournalEntry)
        .filter(
            JournalEntry.id == entry_id
        )
        .first()
    )

    if not entry:

        raise HTTPException(
            status_code=404,
            detail="Journal entry not found."
        )

    db.delete(entry)
    db.commit()

    return {

        "message":
            "Journal entry deleted."
    }


# ============================================================
# CHECK-IN - GET CASE DETAILS
# ============================================================

@app.get("/checkin/{case_id}")
def get_checkin_case(
    case_id: int,
    db: Session = Depends(get_db)
):

    case = (
        db.query(RiskCase)
        .filter(
            RiskCase.id == case_id
        )
        .first()
    )

    if not case:

        raise HTTPException(
            status_code=404,
            detail="Risk case not found."
        )

    employee = (
        db.query(Employee)
        .filter(
            Employee.id == case.employee_id
        )
        .first()
    )

    return {

        "case_id":
            case.id,

        "employee_id":
            case.employee_id,

        "employee_name":
            employee.name
            if employee
            else "Unknown",

        "employee_email":
            employee.email
            if employee
            else "",

        "risk_score":
            case.risk_score,

        "risk_level":
            case.risk_level,

        "signals":
            (
                json.loads(case.signals)
                if case.signals
                else []
            ),

        "status":
            case.status,

        "employee_contacted":
            bool(
                case.employee_contacted
            ),

        "support_required":
            bool(
                case.support_required
            ),

        "responder_notes":
            case.responder_notes
            or "",

        "acknowledged_at":
            case.acknowledged_at
    }


# ============================================================
# CHECK-IN - SUBMIT CHECK-IN
# ============================================================

@app.post("/checkin/{case_id}/submit")
def submit_checkin(
    case_id: int,
    request: CheckinRequest,
    db: Session = Depends(get_db)
):

    case = (
        db.query(RiskCase)
        .filter(
            RiskCase.id == case_id
        )
        .first()
    )

    if not case:

        raise HTTPException(
            status_code=404,
            detail="Risk case not found."
        )

    # --------------------------------------------------------
    # Save employee contact status
    # --------------------------------------------------------

    case.employee_contacted = (
        1
        if request.employee_contacted
        else 0
    )

    case.support_required = (
        1
        if request.support_required
        else 0
    )

    # --------------------------------------------------------
    # Save responder check-in notes
    # --------------------------------------------------------

    case.responder_notes = (
        request.checkin_notes.strip()
    )

    # --------------------------------------------------------
    # Decide workflow outcome
    # --------------------------------------------------------

    if request.outcome == "escalate":

        case.status = "in_progress"

        case.escalation_level = (
            "secondary_responder"
        )

        case.escalation_reason = (
            request.checkin_notes.strip()
            if request.checkin_notes.strip()
            else "Support required after check-in."
        )

        case.escalated_at = (
            datetime.utcnow()
        )

    elif request.outcome == "resolve":

        case.status = "resolved"

        case.resolved_at = (
            datetime.utcnow()
        )

    else:

        case.status = "in_progress"

    db.commit()
    db.refresh(case)

    return {

        "message":
            "Check-in recorded successfully.",

        "case_id":
            case.id,

        "status":
            case.status,

        "employee_contacted":
            bool(
                case.employee_contacted
            ),

        "support_required":
            bool(
                case.support_required
            ),

        "escalation_level":
            case.escalation_level,

        "resolved_at":
            case.resolved_at
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {

        "status":
            "ok",

        "wellora":
            True,

        "ai_enabled":
            client is not None
    }