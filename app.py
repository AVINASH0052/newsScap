import streamlit as st
import requests

st.title("News Sentiment Analyzer")
company = st.text_input("Enter Company Name")

if st.button("Analyze"):
    response = requests.post("http://localhost:8000/process", json={"company_name": company})
    data = response.json()
    
    st.header("Articles")
    for article in data["articles"]:
        st.subheader(article["title"])
        st.write(article["summary"])
        st.write(f"Sentiment: {article['sentiment']}")
    
    st.header("Comparative Analysis")
    positive = sum(1 for a in data["articles"] if a["sentiment"] == "Positive")
    st.write(f"Positive: {positive}, Negative: {10-positive}")
    
    st.header("Hindi TTS")
    st.audio(data["tts_path"])
