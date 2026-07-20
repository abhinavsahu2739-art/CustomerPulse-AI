import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        st.error("❌ GROQ_API_KEY not found.")
        st.stop()

client = Groq(api_key=api_key)


def analyze_review(review):

    prompt = f"""
You are a Customer Experience Analyst.

Analyze the following customer review.

Review:
{review}

Return in Markdown.

# 😊 Sentiment

# 📦 Category

# ⚠ Severity

# 📝 Reason

Category should be one of:
- Delivery
- Product
- Packaging
- Service
- Price
- Other

Severity:
Low / Medium / High
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def analyze_dataset(df):

    reviews = "\n".join(df["review"].head(50).tolist())
    prompt = f"""
You are a Senior Customer Experience Consultant.

Analyze these customer reviews.

Customer Reviews:
{reviews}

Return the report in Markdown using EXACTLY these sections:

# 📋 Executive Summary

# 🔥 Top Complaints

# 😊 Positive Highlights

# ⚠ Business Risks

# 🚀 Growth Opportunities

# ✅ Recommended Actions

Keep the report under 300 words.
Focus on business decisions.
"""

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)
    return response.choices[0].message.content
def ask_ai(question, df):

    reviews = "\n".join(df["review"].head(100).tolist())

    prompt = f"""
You are a Business Intelligence Assistant.

Customer Reviews:
{reviews}

Answer this question:

{question}

Keep the answer concise.
Use markdown.
Give business recommendations whenever possible.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content