import streamlit as st
import requests
import base64
from utils import scrape_news, analyze_sentiment, extract_topics, compare_analysis, generate_hindi_tts

st.title("News Summarization and Sentiment Analysis")

company = st.text_input("Enter Company Name")

if company:
    articles = scrape_news(company)
    if not articles:
        st.error("No articles found.")
    else:
        for idx, article in enumerate(articles):
            article['sentiment'] = analyze_sentiment(article['content'])
            article['topics'] = extract_topics(article['content'])
        
        st.subheader("Articles Analysis")
        for article in articles:
            st.write(f"**Title**: {article['title']}")
            st.write(f"**Summary**: {article['summary']}")
            st.write(f"**Sentiment**: {article['sentiment']}")
            st.write(f"**Topics**: {', '.join(article['topics'])}")
            st.markdown("---")
        
        comparative = compare_analysis(articles)
        st.subheader("Comparative Analysis")
        st.write(f"Sentiment Distribution: {comparative['sentiment_distribution']}")
        for comp in comparative['comparisons']:
            st.write(comp)
        
        summary = " ".join([a['summary'] for a in articles])
        audio_path, hindi_summary = generate_hindi_tts(summary)
        st.subheader("Hindi Summary Speech")
        st.audio(audio_path)
        st.write(f"**Hindi Summary**: {hindi_summary}")
