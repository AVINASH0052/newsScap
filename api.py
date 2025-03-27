from fastapi import FastAPI
from pydantic import BaseModel
from utils import scrape_news, analyze_sentiment, extract_topics, compare_analysis, generate_hindi_tts

app = FastAPI()

class CompanyRequest(BaseModel):
    company: str

@app.post("/analyze")
async def analyze_news(request: CompanyRequest):
    articles = scrape_news(request.company)
    for article in articles:
        article['sentiment'] = analyze_sentiment(article['content'])
        article['topics'] = extract_topics(article['content'])
    comparative = compare_analysis(articles)
    summary = " ".join([a['summary'] for a in articles])
    audio_path, hindi_summary = generate_hindi_tts(summary)
    return {
        "articles": articles,
        "comparative": comparative,
        "audio_path": audio_path,
        "hindi_summary": hindi_summary
    }
