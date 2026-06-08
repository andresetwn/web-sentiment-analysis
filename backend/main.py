from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd

from collections import Counter

from preprocessing import (
    clean_text_bert,
    clean_text_lda
)
from sentiment import analyze_sentiment
from topic import generate_topics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API Running"}

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    df = pd.read_csv(file.file)

    # ambil kolom review
    texts = df['review'].astype(str).tolist()
   # preprocessing untuk IndoBERT
    # preprocessing untuk IndoBERT
    bert_texts = [
        clean_text_bert(text)
        for text in texts
    ]

    # preprocessing untuk LDA
    lda_texts = [
        clean_text_lda(text)
        for text in texts
    ]

    # sentiment
    sentiments = analyze_sentiment(
        bert_texts
    )

    results = []
    labels = []

    for i in range(len(texts)):

        label = sentiments[i]['label']
        score = sentiments[i]['score']

        labels.append(label)

        results.append({
            "review": texts[i],
            "cleaned_text": bert_texts[i],
            "sentiment": label,
            "score": score
        })
    # summary
    summary = dict(Counter(labels))
    # lda
    topics = generate_topics(lda_texts)

    return {
        "summary": summary,
        "topics": topics,
        "results": results
    }