from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(
    "sqlite:///salonDB.db",
    echo=False
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()