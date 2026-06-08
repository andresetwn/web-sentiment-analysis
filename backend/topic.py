from gensim import corpora
from gensim.models import LdaModel

CUSTOM_TOPIC_STOPWORDS = {
    "nya",
    "aja",
    "banget",
    "mau",
    "baru",
    "makin",
    "hari",
    "jam",
    "baik",
}
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
        ],

        "Kemudahan dan Kepuasan Pengguna": [
            "mudah",
            "cepat",
            "baik",
            "bagus",
            "mantap",
            "praktis",
            "aman",
            "bantu",
            "guna",
            "terimakasih",
            "top",
            "keren",
        ],
    }

    scores = {}

    for category, keywords in topic_categories.items():

        score = 0

        for word in words:
            if word in keywords:
                score += 1

        scores[category] = score

    best_category = max(
        scores,
        key=scores.get
    )

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

    for idx, topic in lda_model.show_topics(
        num_topics=3,
        num_words=10,
        formatted=False
    ):

        words = [
        word
        for word, _ in topic
    if word not in CUSTOM_TOPIC_STOPWORDS
]

        topics.append({
            "topic": idx + 1,
            "title": interpret_topic(words),
            "keywords": words
        })

    return topics