import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Dict

class Ingredient(BaseModel):
    quantity: str
    unit: str
    item: str

class Nutrition(BaseModel):
    calories: int
    protein: str
    carbs: str
    fat: str

class RecipeSchema(BaseModel):
    title: str
    cuisine: str
    prep_time: str
    cook_time: str
    total_time: str
    servings: int
    difficulty: str
    ingredients: List[Ingredient]
    instructions: List[str]
    nutrition_estimate: Nutrition
    substitutions: List[str]
    shopping_list: Dict[str, List[str]]
    related_recipes: List[str]

parser = PydanticOutputParser(pydantic_object=RecipeSchema)

def process_recipe(scraped_text: str):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1, google_api_key=os.getenv("GEMINI_API_KEY"))
    
    # The prompt is now directly in the code. No more reading from a file!
    prompt_text = """You are an expert culinary assistant. I will provide you with raw text scraped from a recipe blog. 
Your job is to extract the recipe data and generate additional insights.

Extract the following:
1. Recipe title
2. Cuisine type
3. Prep time, cook time, total time
4. Servings
5. Ingredients list (MUST be a list of objects with exactly: "quantity", "unit", "item")
6. Step-by-step instructions (MUST be a list of strings)
7. Difficulty level (easy, medium, hard)

Generate the following based on the extracted recipe:
8. Nutritional estimate per serving (calories as integer, protein/carbs/fat as strings like "12g")
9. 3 ingredient substitutions (list of strings)
10. Shopping list grouped by category (e.g., dairy, produce - keys as categories, values as lists)
11. 3 related recipes that pair well (list of strings)

{format_instructions}

SCRAPED TEXT:
{scraped_text}"""

    prompt = PromptTemplate(
        template=prompt_text,
        input_variables=["scraped_text"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain = prompt | llm | parser
    return chain.invoke({"scraped_text": scraped_text}).model_dump()