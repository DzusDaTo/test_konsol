import unittest
from library_manager import Library, Book
import json
import os


class TestLibraryManager(unittest.TestCase):

    def setUp(self):
        """Метод для подготовки данных перед каждым тестом."""
        # Создадим временный файл для тестов
        self.library = Library(filename="test_library.json")
        self.library.books = []  # Очистим список книг для тестов
        self.library.save_books()

    def tearDown(self):
        """Метод для очистки после каждого теста."""
        # Удалим файл, созданный для тестов
        if os.path.exists("test_library.json"):
            os.remove("test_library.json")

    def test_add_book(self):
        """Тест добавления книги."""
        self.library.add_book("Test Book", "Test Author", 2024)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Book")
        self.assertEqual(self.library.books[0].author, "Test Author")
        self.assertEqual(self.library.books[0].year, 2024)
        self.assertEqual(self.library.books[0].status, "в наличии")

    def test_remove_book(self):
        """Тест удаления книги."""
        self.library.add_book("Book to Remove", "Some Author", 2024)
        book_id = self.library.books[0].id
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_search_books(self):
        """Тест поиска книги по названию."""
        self.library.add_book("Searchable Book", "Search Author", 2024)
        results = self.library.search_books("Searchable")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Searchable Book")

    def test_update_status(self):
        """Тест изменения статуса книги."""
        self.library.add_book("Status Test Book", "Status Author", 2024)
        book_id = self.library.books[0].id
        self.library.update_status(book_id, "выдана")
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_invalid_update_status(self):
        """Тест неправильного обновления статуса книги."""
        self.library.add_book("Invalid Status Book", "Author", 2024)
        book_id = self.library.books[0].id
        self.library.update_status(book_id, "invalid status")  # Некорректный статус
        self.assertEqual(self.library.books[0].status, "в наличии")  # Статус не должен измениться

    def test_remove_nonexistent_book(self):
        """Тест удаления несуществующей книги."""
        self.library.add_book("Test Book", "Author", 2024)
        self.library.remove_book(999)  # Несуществующий ID
        self.assertEqual(len(self.library.books), 1)  # Книга не должна быть удалена


if __name__ == '__main__':
    unittest.main()
