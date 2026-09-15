from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = (BASE_DIR / "data" / "app.db").resolve()
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    f"sqlite:///{str(DB_PATH).replace('\\', '/')}",
    echo=False,
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()