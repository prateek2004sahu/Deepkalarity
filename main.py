from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import SessionLocal, Recipe
from scraper import scrape_url
from llm_handler import process_recipe
from datetime import datetime

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

class UrlInput(BaseModel):
    url: str

@app.post("/api/extract")
def extract_recipe(data: UrlInput):
    db = SessionLocal()
    try:
        # 1. Scrape
        raw_text = scrape_url(data.url)
        
        # 2. LLM Process
        recipe_data = process_recipe(raw_text)
        
        # 3. Store in DB
        db_recipe = Recipe(url=data.url, **recipe_data)
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        
        return db_recipe
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/api/recipes")
def get_recipes():
    db = SessionLocal()
    recipes = db.query(Recipe).order_by(Recipe.created_at.desc()).all()
    db.close()
    return recipes

@app.get("/api/recipes/{recipe_id}")
def get_recipe(recipe_id: int):
    db = SessionLocal()
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    db.close()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe