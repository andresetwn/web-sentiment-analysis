import re

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

stop_factory = StopWordRemoverFactory()
stopwords = stop_factory.create_stop_word_remover()

stem_factory = StemmerFactory()
stemmer = stem_factory.create_stemmer()

CUSTOM_STOPWORDS = {
    "aplikasi",
    "octo",
    "mobile",
    "cimb",
    "niaga",
    "bank",

    "yg",
    "nya",
    "aja",
    "nih",
    "dong",

    "ga",
    "gak",
    "enggak",

    "sangat",
    "lebih",
    "buat",
    "jadi",
    "udah",
    "masih",

    "di",
    "ke",
    "dari",
    "yang"
}

# =========================
# UNTUK INDOBERT
# =========================

def clean_text_bert(text):

    text = str(text).lower()

    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)

    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# =========================
# UNTUK LDA
# =========================

def clean_text_lda(text):

    text = str(text).lower()

    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)

    text = re.sub(r'\d+', '', text)

    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    text = stopwords.remove(text)

    text = stemmer.stem(text)

    text = re.sub(r'\s+', ' ', text)
    words = text.split()

    words = [
        word
        for word in words
        if word not in CUSTOM_STOPWORDS
    ]

    text = " ".join(words)

    return text.strip()