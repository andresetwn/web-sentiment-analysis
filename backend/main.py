from collections import Counter
from urllib import request

import pandas as pd
from scraper import scrape_reviews
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from preprocessing import clean_text_bert, clean_text_lda
from sentiment import analyze_sentiment
from topic import generate_topics
from datetime import datetime
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from io import BytesIO

buffer = BytesIO()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

class ScrapeRequest(BaseModel):
    review_count: int = 3000
    newest: bool = True
    start_date: str | None = None
    end_date: str | None = None

@app.get("/")
def home():
    return {"message": "API Running"}

@app.post("/scrape")
async def scrape_dataset(request: ScrapeRequest):
    df = scrape_reviews(
        review_count=request.review_count,
        newest=request.newest,
        start_date=request.start_date,
        end_date=request.end_date,
    )
    today = datetime.now().strftime("%Y%m%d")
    if request.newest:
        filename = (
            f"dataset_octo_mobile_terbaru_{today}.csv"
        )
    else:
        start = request.start_date.replace("-", "")
        end = request.end_date.replace("-", "")
        filename = (
            f"dataset_octo_mobile_{start}_{end}.csv"
        )
    df.to_csv(
        buffer,
        index=False,
        encoding="utf-8-sig"
    )
    buffer.seek(0)

    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        },
    )

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    df = pd.read_csv(file.file)

    # DATA PREPARATION
    total_before = len(df)
    missing_count = df.isna().any(axis=1).sum()
    duplicate_count = df.duplicated().sum()
    df = df.dropna(subset=["review"])
    df = df[df["review"].str.strip() != ""]
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)
    total_after = len(df)
  
    # PREPROCESSING
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

    # SENTIMEN
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
    topics, topic_summary = generate_topics(lda_texts)

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