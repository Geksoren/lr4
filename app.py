from flask import Flask, render_template, request
from collections import Counter
import re

app = Flask(__name__)

def clean_text(text):
    # Удаляем все знаки препинания, заменяя их пробелами
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    return cleaned_text

def find_most_common_words(text):
    # Используем чистый текст для разбиения на слова
    cleaned_text = clean_text(text.lower())
    words = re.findall(r'\b\w+\b', cleaned_text)

    # Считаем частоту каждого слова
    word_counts = Counter(words)

    # Находим максимальное количество повторений
    max_count = max(word_counts.values())

    # Возвращаем список слов, которые имеют максимальное количество повторений
    most_common_words = [(word, count) for word, count in word_counts.items() if count == max_count]

    return most_common_words

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            text = file.read().decode('utf-8')
            most_common_words = find_most_common_words(text)
            return render_template('result.html', most_common_words=most_common_words)
    return render_template('index.html')


app.run(debug=True)