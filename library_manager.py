import json


class Book:
    def __init__(self, title, author, year, status="в наличии"):
        """
            Инициализирует книгу с указанными аттрибутами.

            :param title: Название книги.
            :param author: Автор книги.
            :param year: Год издания книги.
            :param status: Статус книги (по умолчанию "в наличии").
        """
        self.id = None
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        """
            Возвращает строковое представление книги.

            :return: Строка с информацией о книге.
        """
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Status: {self.status}"


class Library:
    def __init__(self, filename="library.json"):
        """
            Инициализирует библиотеку и загружает книги из файла.

            :param filename: Имя файла для хранения данных о книгах.
        """
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        """
            Загружает книги из файла.

            :return: Список книг.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                books_data = json.load(file)
                books = []
                for data in books_data:
                    book = Book(data['title'], data['author'], data['year'], data['status'])
                    book.id = data['id']
                    books.append(book)
                return books
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self):
        """
            Сохраняет все книги в файл.
        """
        with open(self.filename, "w", encoding="utf-8") as file:
            books_data = [{'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year, 'status': book.status} for book in self.books]
            json.dump(books_data, file, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        """
            Добавляет новую книгу в библиотеку.

            :param title: Название книги.
            :param author: Автор книги.
            :param year: Год издания книги.
        """
        book = Book(title, author, year)
        book.id = len(self.books) + 1  # Уникальный ID
        self.books.append(book)
        self.save_books()

    def remove_book(self, book_id):
        """
            Удаляет книгу по ID.

            :param book_id: ID книги для удаления.
        """
        book = self.get_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def get_book_by_id(self, book_id):
        """
            Ищет книгу по ID.

            :param book_id: ID книги.
            :return: Книга с заданным ID или None, если книга не найдена.
        """
        return next((book for book in self.books if book.id == book_id), None)

    def search_books(self, query):
        """
            Ищет книги по названию, автору или году издания.

            :param query: Поисковой запрос.
            :return: Список найденных книг.
        """
        found_books = [book for book in self.books if query.lower() in book.title.lower() or query.lower() in book.author.lower() or query.lower() in str(book.year)]
        return found_books

    def display_books(self):
        """
        Отображает все книги в библиотеке.
        """
        if self.books:
            for book in self.books:
                print(book)
        else:
            print("Библиотека пуста.")

    def update_status(self, book_id: int, status: str):
        """
        Обновляет статус книги по ID.

        :param book_id: ID книги для изменения статуса.
        :param status: Новый статус книги.
        """
        book = self.get_book_by_id(book_id)
        if book:
            if status in ["в наличии", "выдана"]:
                book.status = status
                self.save_books()
            else:
                print("Неверный статус. Доступные статусы: 'в наличии', 'выдана'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")


def main():
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = input("Введите год издания: ")
            library.add_book(title, author, year)
            print("Книга добавлена.")

        elif choice == "2":
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)

        elif choice == "3":
            query = input("Введите поисковый запрос (название, автор, год): ")
            found_books = library.search_books(query)
            if found_books:
                for book in found_books:
                    print(book)
            else:
                print("Книги не найдены.")

        elif choice == "4":
            library.display_books()

        elif choice == "5":
            book_id = int(input("Введите ID книги для изменения статуса: "))
            status = input("Введите новый статус ('в наличии' или 'выдана'): ")
            library.update_status(book_id, status)

        elif choice == "6":
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
