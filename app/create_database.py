from app.database import Base, engine
import app.models
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)