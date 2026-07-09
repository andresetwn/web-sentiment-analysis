from collections import Counter

from gensim import corpora
from gensim.models import LdaModel


def interpret_topic(words):

    topic_categories = {
        "Kendala Login dan Akses": [
            "login",
            "otp",
            "verifikasi",
            "akses",
            "maintenance",
            "masuk",
            "aktivasi",
            "blokir",
        ],

        "Permasalahan Sistem Aplikasi": [
            "error",
            "eror",
            "bug",
            "crash",
            "ganggu",
            "gagal",
            "loading",
            "lemot",
            "update",
            "force",
            "close",
        ],

        "Layanan Transaksi Perbankan": [
            "transfer",
            "transaksi",
            "saldo",
            "rekening",
            "atm",
            "bayar",
            "pembayaran",
            "tarik",
            "kirim",
            "qris",
        ],

        "Kemudahan dan Kepuasan Pengguna": [
            "mudah",
            "cepat",
            "praktis",
            "aman",
            "bantu",
            "keren",
            "top",
        ],
    }

    scores = {}

    for category, keywords in topic_categories.items():
        score = 0
        for word in words:
            if word in keywords:
                score += 1
        scores[category] = score
    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "Topik Umum Pengguna"

    return best_category


def generate_topics(texts):

    tokenized = [text.split() for text in texts]
    dictionary = corpora.Dictionary(tokenized)

    corpus = [
        dictionary.doc2bow(text)
        for text in tokenized
    ]
    lda_model = LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=3,
        passes=20,
        random_state=42
    )

    topics = []
    topic_counter = Counter()
    lda_topics = lda_model.show_topics(
        num_topics=3,
        num_words=3,
        formatted=False
    )

    for idx, topic in lda_topics:

        words = [
            word
            for word, _ in topic
        ]
        title = interpret_topic(words)
        topics.append({
            "topic": idx + 1,
            "title": title,
            "keywords": words
        })

    # PERHITUNGAN DISTRIBUSI TOPIK
    for bow in corpus:
        topic_probs = lda_model.get_document_topics(bow)
        dominant_topic = max(
            topic_probs,
            key=lambda x: x[1]
        )[0]
        title = topics[dominant_topic]["title"]
        topic_counter[title] += 1

    topic_summary = dict(topic_counter)

    return topics, topic_summary