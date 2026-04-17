import requests
from bs4 import BeautifulSoup
from fastapi import HTTPException

def scrape_url(url: str) -> str:
    try:
        # CHECK IF IT'S A LOCAL FILE (Our workaround for paywalls)
        if url.startswith("file://") or url.startswith("test_recipe"):
            # Extract filename if needed, but for now we hardcode the path for easy testing
            file_path = "D:/DeepKlarity_Assignment/frontend/test_recipe.html"
            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        else:
            # Normal web scraping for real URLs
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            html_content = response.text
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for script in soup(["script", "style", "header", "footer", "nav"]):
            script.extract()
            
        text = soup.get_text(separator='\n', strip=True)
        
        if len(text) < 50:
            raise ValueError("Extracted text is too short. Not a valid recipe.")
            
        return text
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Could not find local test_recipe.html. Make sure it's in the frontend folder!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to scrape URL: {str(e)}")