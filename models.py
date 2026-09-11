from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base


# =====================================================
# EMPLOYEE
# =====================================================

class Employee(Base):

    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="employee"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =====================================================
# GAME RESULTS
# =====================================================

class GameResult(Base):

    __tablename__ = "game_results"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id = Column(
        Integer,
        nullable=False
    )

    game_name = Column(
        String,
        nullable=False
    )

    time_taken = Column(
        Integer,
        nullable=True
    )

    correct = Column(
        Integer,
        nullable=True
    )

    wrong = Column(
        Integer,
        nullable=True
    )

    accuracy = Column(
        Integer,
        nullable=True
    )

    score = Column(
        Integer,
        nullable=True
    )

    # Game-specific information
    # stored as JSON text

    metrics = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =====================================================
# RISK CASE
# =====================================================

class RiskCase(Base):

    __tablename__ = "risk_cases"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # -------------------------------------------------
    # Employee
    # -------------------------------------------------

    employee_id = Column(
        Integer,
        nullable=False
    )

    # -------------------------------------------------
    # Risk information
    # -------------------------------------------------

    risk_score = Column(
        Integer,
        nullable=False
    )

    risk_level = Column(
        String,
        nullable=False
    )

    # Signals detected by Risk Engine

    signals = Column(
        Text,
        nullable=True
    )

    # -------------------------------------------------
    # Case workflow
    # -------------------------------------------------

    status = Column(
        String,
        default="new"
    )

    # -------------------------------------------------
    # Responder
    # -------------------------------------------------

    responder_id = Column(
        Integer,
        nullable=True
    )

    responder_notes = Column(
        Text,
        nullable=True
    )

    # -------------------------------------------------
    # Escalation
    # -------------------------------------------------

    escalation_level = Column(
        String,
        default="none"
    )

    escalation_reason = Column(
        Text,
        nullable=True
    )

    escalated_at = Column(
        DateTime,
        nullable=True
    )

    # -------------------------------------------------
    # Safety workflow
    # -------------------------------------------------

    employee_contacted = Column(
        Integer,
        default=0
    )

    support_required = Column(
        Integer,
        default=0
    )

    # -------------------------------------------------
    # Timestamps
    # -------------------------------------------------

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    acknowledged_at = Column(
        DateTime,
        nullable=True
    )

    resolved_at = Column(
        DateTime,
        nullable=True
    )

# =====================================================
# PRIVATE JOURNAL
# =====================================================

class JournalEntry(Base):

    __tablename__ = "journal_entries"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Employee who owns the journal entry
    employee_id = Column(
        Integer,
        nullable=False
    )

    # Private journal content
    content = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )