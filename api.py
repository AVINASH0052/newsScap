from fastapi import FastAPI
from pydantic import BaseModel
from utils import scrape_news, analyze_sentiment, generate_tts

app = FastAPI()

class CompanyRequest(BaseModel):
    company_name: str

@app.post("/process")
async def process_news(request: CompanyRequest):
    company = request.company_name
    articles = scrape_news(company)
    analyzed_articles = analyze_sentiment(articles)
    tts_path = generate_tts(analyzed_articles)
    return {"articles": analyzed_articles, "tts_path": tts_path}
