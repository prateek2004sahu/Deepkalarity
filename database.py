from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_5vlsdOjWoNY1@ep-hidden-paper-amur6xti.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require")

# Add connect_args for cloud SSL
engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"} if "neon.tech" in DATABASE_URL or "sslmode" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ... keep the rest of the Recipe class exactly the same ...
class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    title = Column(String)
    cuisine = Column(String)
    prep_time = Column(String)
    cook_time = Column(String)
    total_time = Column(String)
    servings = Column(Integer)
    difficulty = Column(String)
    ingredients = Column(JSON) # Stores list of dicts
    instructions = Column(JSON) # Stores list of strings
    nutrition_estimate = Column(JSON) # Stores dict
    substitutions = Column(JSON) # Stores list
    shopping_list = Column(JSON) # Stores dict
    related_recipes = Column(JSON) # Stores list
    created_at = Column(DateTime, server_default="now()")

Base.metadata.create_all(bind=engine)