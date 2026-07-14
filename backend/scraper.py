from datetime import datetime

import pandas as pd

from google_play_scraper import (
    Sort,
    reviews,
)
APP_ID = "id.co.cimbniaga.mobile.android"

def scrape_reviews(
    review_count: int = 3000,
    newest: bool = True,
    start_date: str | None = None,
    end_date: str | None = None,
):
    all_reviews = []
    continuation_token = None
    sort = Sort.NEWEST if newest else Sort.NEWEST
    start = (
        datetime.strptime(start_date, "%Y-%m-%d")
        if start_date
        else None
    )
    end = (
        datetime.strptime(end_date, "%Y-%m-%d")
        if end_date
        else None
    )
    stop_scraping = False
    while len(all_reviews) < review_count:
        result, continuation_token = reviews(
            APP_ID,
            lang="id",
            country="id",
            sort=sort,
            count=200,
            continuation_token=continuation_token,
        )
        if not result:
            break
        for review in result:
            review_date = review["at"]
            if not newest:
                if start and review_date < start:
                    stop_scraping = True
                    break
                if end and review_date > end:
                    continue
            all_reviews.append(review)
            if len(all_reviews) >= review_count:
                break
        if stop_scraping:
            break
        if continuation_token is None:
            break
    df = pd.DataFrame([
    {
        "userName": review["userName"],
        "review": review["content"],
        "rating": review["score"],
        "at": review["at"],
    }
    for review in all_reviews
])

    return df