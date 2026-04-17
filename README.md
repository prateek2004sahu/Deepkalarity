DeepKlarity - Recipe Extractor & Meal Planner
Objective
A full-stack application that accepts a recipe blog URL, scrapes the content using BeautifulSoup, and uses a Large Language Model (LLM) via LangChain to extract structured recipe data, nutritional estimates, substitutions, and a shopping list. The data is stored in PostgreSQL and displayed in a clean, card-based UI.

Tech Stack
Backend: FastAPI, Python
Database: PostgreSQL (Neon Cloud)
Frontend: Vanilla HTML, CSS, and JavaScript
LLM: Google Gemini (via LangChain & gemini-1.5-flash)
Scraping: BeautifulSoup, Requests
Project Structure
DeepKlarity_Assignment/├── backend/│   ├── main.py           # FastAPI endpoints│   ├── database.py       # SQLAlchemy DB models & setup│   ├── scraper.py        # BeautifulSoup web scraper│   ├── llm_handler.py    # LangChain logic & Pydantic parsing│   └── requirements.txt  # Python dependencies├── frontend/│   ├── index.html        # Main UI (Tabs 1 & 2)│   ├── style.css         # Card-based minimal styling│   ├── app.js            # Frontend logic & API calls│   └── test_recipe.html  # Local HTML used for testing (bypasses paywalls)├── prompts/│   └── recipe_prompt.txt # LangChain prompt template used for extraction├── sample_data/│   └── grilled_cheese_output.json # Sample API JSON response├── screenshots/          # UI testing evidence│   ├── tab1_extraction.png│   ├── tab2_history.png│   └── details_modal.png└── README.md             # You are here
Setup & Installation
1. Backend Setup
bash

# Navigate to the backend folder
cd backend

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # (Windows)

# Install dependencies
pip install -r requirements.txt
2. Environment Variables
Set the following environment variables in your terminal before running the server:

GEMINI_API_KEY: Your free Google Gemini API key.
DATABASE_URL: Your PostgreSQL connection string (e.g., postgresql://user:password@localhost:5432/recipe_db).
Windows PowerShell Example:

powershell

 $env:GEMINI_API_KEY="your_gemini_api_key_here"
 $env:DATABASE_URL="postgresql://postgres:password@localhost:5432/recipe_db"
3. Run the Backend Server
bash

uvicorn main:app --reload
The server will start on http://127.0.0.1:8000 and automatically create the database tables.

4. Run the Frontend
Open the frontend/index.html file using the Live Server extension in VS Code, or simply double-click the file to open it in your browser.

API Endpoints
1. Extract Recipe
URL: POST /api/extract
Body: { "url": "string" }
Description: Scrapes the provided URL, processes it through the LLM using strict Pydantic formatting, stores it in PostgreSQL, and returns the structured JSON.
2. Get All Saved Recipes
URL: GET /api/recipes
Description: Returns an array of all previously processed recipes for the History tab.
3. Get Single Recipe Details
URL: GET /api/recipes/{id}
Description: Fetches a single recipe by its ID to populate the Details modal.
