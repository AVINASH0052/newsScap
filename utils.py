import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from gtts import gTTS
import os

def scrape_news(company):
    url = f"https://news.google.com/search?q={company}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    for item in soup.find_all('article', limit=10):
        title = item.find('a', class_='DY5T1d').text
        summary = item.find('div', class_='xBbh9').text
        articles.append({"title": title, "summary": summary})
    return articles

def analyze_sentiment(articles):
    sia = SentimentIntensityAnalyzer()
    for article in articles:
        score = sia.polarity_scores(article["summary"])
        if score['compound'] >= 0.05:
            article["sentiment"] = "Positive"
        elif score['compound'] <= -0.05:
            article["sentiment"] = "Negative"
        else:
            article["sentiment"] = "Neutral"
    return articles

def generate_tts(articles):
    translator = Translator()
    hindi_text = translator.translate(str(articles), dest='hi').text
    tts = gTTS(text=hindi_text, lang='hi')
    tts.save("output.mp3")
    return "output.mp3"
