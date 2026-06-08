from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="./models/indobert-octo"
)

LABEL_MAP = {
    "LABEL_0": "negative",
    "LABEL_2": "positive"
}

def analyze_sentiment(texts):

    results = classifier(texts)

    output = []

    for r in results:

        score = float(r["score"])

        if score < 0.75:
            sentiment = "neutral"
        else:
            sentiment = LABEL_MAP.get(
                r["label"],
                "neutral"
            )

        output.append({
            "label": sentiment,
            "score": score
        })

    return output