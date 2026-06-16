from collections import Counter

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from preprocessing import clean_text_bert, clean_text_lda
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

    # Baca dataset
    df = pd.read_csv(file.file)

    # Ambil kolom review
    texts = df["review"].astype(str).tolist()

    # Preprocessing untuk IndoBERT
    bert_texts = [
        clean_text_bert(text)
        for text in texts
    ]

    # Preprocessing untuk LDA
    lda_texts = [
        clean_text_lda(text)
        for text in texts
    ]

    # Analisis sentimen menggunakan IndoBERT
    sentiments = analyze_sentiment(bert_texts)

    results = []
    labels = []

    for original_text, cleaned_text, sentiment in zip(
        texts,
        bert_texts,
        sentiments,
    ):
        labels.append(sentiment["label"])

        results.append({
            "review": original_text,
            "cleaned_text": cleaned_text,
            "sentiment": sentiment["label"],
            "score": sentiment["score"],
        })

    # Ringkasan jumlah sentimen
    summary = dict(Counter(labels))

    # Topic Modeling menggunakan hasil preprocessing LDA
    topics = generate_topics(lda_texts)

    return {
        "summary": summary,
        "topics": topics,
        "results": results,
    }