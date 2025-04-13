import streamlit as st
from transformers import pipeline
import re


st.set_page_config(page_title="Text Summarizer", layout="centered")

# Load summarization pipeline
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()


st.title("✨Text Summarizer")

# Text input field
user_input = st.text_area("✍️ Enter your text for summarization:", height=200)

# Preprocessing text
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^\w\s]', '', text)  
    return text

if st.button("Generate Concise Summary"):
    if not user_input or len(user_input.split()) < 20:
        st.warning("⚠️ Please enter at least 20 words to generate a summary.")
    else:
        try:
            
            user_input = preprocess_text(user_input)
            word_count = len(user_input.split())  
            
            
            max_len = min(120, int(word_count * 0.5))  
            result = summarizer(user_input, max_length=max_len, min_length=40, do_sample=False)
            summary_text = result[0]['summary_text']

            
            sentences = summary_text.split(". ")
            three_sentences = '. '.join(sentences[:3])
            if not three_sentences.endswith('.'):
                three_sentences += '.'

           
            summary_word_count = len(three_sentences.split())

            
            st.subheader("🔑 Your 3-Line Summary")
            st.success(three_sentences)

            
            st.info(f"📜 Original Text: **{word_count}** words | 📄 Summary: **{summary_word_count}** words")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
