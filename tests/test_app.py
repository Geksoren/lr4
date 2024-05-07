import unittest
from flask_testing import TestCase
from flask import Flask
from io import BytesIO
from app import app, find_most_common_words

class TestApp(TestCase):
    # Инициализация тестового приложения Flask
    def create_app(self):
        app.config['TESTING'] = True
        return app

    # Тест главной страницы
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Поиск самого частого слова', response.data.decode('utf-8'))

    # Тест загрузки файла и проверки самых частых слов
    def test_file_upload_and_common_words(self):
        data = {
            'file': (BytesIO(b'hello hello world world'), 'test.txt')
        }
        response = self.client.post('/', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn('hello (2 раз)', response.data.decode('utf-8'))
        self.assertIn('world (2 раз)', response.data.decode('utf-8'))

    # Тестирование на регистр
    def test_find_most_common_words_case_insensitive(self):
        text = "Привет как дела привет"
        result = find_most_common_words(text)
        expected_result = [('привет', 2)]
        self.assertEqual(sorted(result), sorted(expected_result))

    # Тестирование на знаки препинания
    def test_find_most_common_words_ignore_punctuation(self):
        text = "привет, как дела, привет"
        result = find_most_common_words(text)
        expected_result = [('привет', 2)]
        self.assertEqual(sorted(result), sorted(expected_result))

    # Тестирование на несколько самых частых слов
    def test_find_most_common_words_multiple_most_common(self):
        text = "привет, как дела дела, привет"
        result = find_most_common_words(text)
        expected_result = [('привет', 2), ('дела', 2)]
        self.assertEqual(sorted(result), sorted(expected_result))

# Запуск тестов
if __name__ == '__main__':
    unittest.main()

