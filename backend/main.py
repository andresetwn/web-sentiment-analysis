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

    df = pd.read_csv(file.file)

    # ==========================
    # DATA PREPARATION
    # ==========================

    total_before = len(df)
    missing_count = df.isna().any(axis=1).sum()
    duplicate_count = df.duplicated().sum()
    # Hapus missing value
    df = df.dropna(subset=["review"])
    # Hapus review kosong
    df = df[df["review"].str.strip() != ""]
    # Hapus duplikat
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    total_after = len(df)

    # ==========================
    # PREPROCESSING
    # ==========================
    texts = df["review"].astype(str).tolist()
    bert_texts = [
        clean_text_bert(text)
        for text in texts
    ]
    lda_texts = [
        clean_text_lda(text)
        for text in texts
    ]
    df["clean_review_bert"] = bert_texts
    df["clean_review_lda"] = lda_texts

    # ==========================
    # SENTIMENT
    # ==========================
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

    summary = dict(Counter(labels))

    # ==========================
    # TOPIC MODELING
    # ==========================

    topics, topic_summary = generate_topics(lda_texts)

    # ==========================
    # RETURN
    # ==========================

    return {

        "preprocessing": {
            "total_before": total_before,
            "missing": int(missing_count),
            "duplicate": int(duplicate_count),
            "total_after": total_after,
        },
        "summary": summary,
        "topic_summary": topic_summary,
        "topics": topics,
        "results": results,
    }