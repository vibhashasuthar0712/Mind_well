from database import engine
from sqlalchemy import inspect, text

inspector = inspect(engine)

columns = [column["name"] for column in inspector.get_columns("journal_entries")]

if "feeling_after" not in columns:
    with engine.begin() as conn:
        conn.execute(
            text("ALTER TABLE journal_entries ADD COLUMN feeling_after VARCHAR")
        )
    print("SUCCESS: feeling_after column added.")
else:
    print("INFO: feeling_after column already exists.")