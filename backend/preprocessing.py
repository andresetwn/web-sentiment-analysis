import re

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

stop_factory = StopWordRemoverFactory()
stopwords = stop_factory.create_stop_word_remover()
stem_factory = StemmerFactory()
stemmer = stem_factory.create_stemmer()

CUSTOM_STOPWORDS = {
    # Nama aplikasi / perusahaan
    "aplikasi",
    "octo",
    "mobile",
    "cimb",
    "niaga",
    "bank",

    # Kata informal
    "yg",
    "nya",
    "aja",
    "nih",
    "dong",
    "ga",
    "gak",
    "enggak",

    # Kata umum
    "yang",
    "dan",
    "di",
    "ke",
    "dari",
    "untuk",
    "dengan",
    "pada",
    "jadi",
    "buat",
    "agar",

    # Kata intensitas
    "sangat",
    "lebih",
    "banget",
    "cukup",
    "sekali",

    # Kata waktu
    "hari",
    "jam",
    "bulan",
    "tahun",
    "lama",
    "baru",

    # Kata yang kurang bermakna sebagai topik
    "mau",
    "masih",
    "udah",
    "bisa",
    "makin",
    "malah",
    "baik",
    "mantap",
    "bagus",
    "guna",
    "terimakasih",
     "terus",
    "sering",
    "padahal",
    "apa",
    "kalo",
    "kalau",
    "pake",
    "pakai",
    "semua",
    "banyak",
    "siang",
    "good",
    "tiba",
    "suka",
    "selalu",
    "puas",
    "kok",
    "mulu",
    "buka",
    "keren",
    
}
def clean_text_bert(text):

    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def clean_text_lda(text):

    text = str(text).lower()
    text = text.replace("eror", "error")
    text = re.sub(r'http\S+', ' ', text)
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
        and len(word) > 2
    ]

    text = " ".join(words)

    return text.strip()