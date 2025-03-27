from bs4 import BeautifulSoup
import requests
from transformers import pipeline
from keybert import KeyBERT
from gtts import gTTS

def scrape_news(company):
    url = f"https://www.reuters.com/search/news?blob={company}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = []
    for link in soup.select('.search-result-title'):
        article_url = 'https://www.reuters.com' + link['href']
        article_resp = requests.get(article_url)
        article_soup = BeautifulSoup(article_resp.text, 'html.parser')
        title = article_soup.find('h1').text.strip()
        summary = article_soup.find('p', class_='Paragraph-paragraph-2Bgue').text.strip()
        content = ' '.join([p.text for p in article_soup.find_all('p', class_='Paragraph-paragraph-2Bgue')])
        articles.append({'title': title, 'summary': summary, 'content': content})
        if len(articles) >= 10:
            break
    return articles

sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
kw_model = KeyBERT()

def analyze_sentiment(text):
    result = sentiment_model(text[:512])[0]
    return {'LABEL_0': 'Negative', 'LABEL_1': 'Neutral', 'LABEL_2': 'Positive'}[result['label']]

def extract_topics(text):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), top_n=3)
    return [kw[0] for kw in keywords]

def compare_analysis(articles):
    sentiments = [a['sentiment'] for a in articles]
    dist = {'Positive': sentiments.count('Positive'), 'Negative': sentiments.count('Negative'), 'Neutral': sentiments.count('Neutral')}
    comparisons = [f"Article {i+1} focuses on {', '.join(a['topics'])}" for i, a in enumerate(articles)]
    return {'sentiment_distribution': dist, 'comparisons': comparisons}

translator = pipeline("translation_en_to_hi", model="Helsinki-NLP/opus-mt-en-hi")
tts = pipeline("text-to-speech", model="facebook/fastspeech2-hi")

def generate_hindi_tts(text):
    summary_en = text[:500]
    summary_hi = translator(summary_en)[0]['translation_text']
    tts = gTTS(text=summary_hi, lang='hi', slow=False)
    audio_path = "output.mp3"
    tts.save(audio_path)
    return audio_path, summary_hi
