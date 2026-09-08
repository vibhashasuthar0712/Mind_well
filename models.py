from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="employee")
    created_at = Column(DateTime, default=datetime.utcnow)


class GameResult(Base):
    __tablename__ = "game_results"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, nullable=False)

    game_name = Column(String, nullable=False)

    # Common activity metrics
    time_taken = Column(Integer, nullable=True)
    correct = Column(Integer, nullable=True)
    wrong = Column(Integer, nullable=True)
    accuracy = Column(Integer, nullable=True)
    score = Column(Integer, nullable=True)

    # Game-specific metrics stored as JSON text
    metrics = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)