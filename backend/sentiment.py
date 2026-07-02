from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="./models/indobert-octo"
)

LABEL_MAP = {
    "LABEL_0": "negatif",
    "LABEL_1": "netral",
    "LABEL_2": "positif"
}

def analyze_sentiment(texts):

    results = classifier(texts)

    output = []

    for r in results:

        sentiment = LABEL_MAP.get(
            r["label"],
            "tidak diketahui"
        )

        output.append({
            "label": sentiment,
            "score": r["score"]
        })

    return output