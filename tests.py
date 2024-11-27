import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_genre, который нам возвращает метод get_books_genre, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # добавление новой книги, включая граничные проверки
    @pytest.mark.parametrize("book_title, expected_in_books, expected_length", [
        ('Машина времени', True, 1),
        ('', False, 0),
    ])
    def test_add_new_book(self, book_title, expected_in_books, expected_length):
        collector = BooksCollector()

        collector.add_new_book(book_title)
        assert (book_title in collector.books_genre) == expected_in_books
        assert len(collector.books_genre) == expected_length

    # у добавленной книги отсутствует жанр
    def test_book_has_no_genre_after_adding(self):
        collector = BooksCollector()
        collector.add_new_book('Сумерки')

        assert collector.books_genre['Сумерки'] == ''

    # проверка установки жанра для книги
    @pytest.mark.parametrize("book_title, genre, expected_genre", [
        ('Машина времени', 'Фантастика', 'Фантастика'),
        ('Сумерки', 'Ужасы', 'Ужасы'),
        ('Олле Лукойе', 'Сказки', ''),
    ])
    def test_set_book_genre(self, book_title, genre, expected_genre):
        collector = BooksCollector()
        collector.add_new_book(book_title)
        collector.set_book_genre(book_title, genre)

        assert collector.books_genre[book_title] == expected_genre

    # фильтрация книг по жанру
    @pytest.mark.parametrize("books_and_genres, genre_to_filter, expected_books", [
        ([('Машина времени', 'Фантастика'), ('Сумерки', 'Фантастика')], 'Фантастика', ['Машина времени', 'Сумерки']),
        ([('Машина времени', 'Фантастика'), ('Сумерки', 'Ужасы')], 'Ужасы', ['Сумерки']),
        ([('Машина времени', 'Фантастика')], 'Комедия', []),
    ])
    def test_get_books_with_specific_genre(self, books_and_genres, genre_to_filter, expected_books):
        collector = BooksCollector()
        for book, genre in books_and_genres:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)

        filtered_books = collector.get_books_with_specific_genre(genre_to_filter)
        assert filtered_books == expected_books

    # возврат списка книг для детей
    def test_get_books_for_children(self):
        collector = BooksCollector()
        collector.add_new_book('Машина времени')
        collector.set_book_genre('Машина времени', 'Фантастика')

        collector.add_new_book('Сумерки')
        collector.set_book_genre('Сумерки', 'Ужасы')

        books_for_children = collector.get_books_for_children()
        assert 'Машина времени' in books_for_children
        assert 'Сумерки' not in books_for_children

    # добавление книги в избранное
    def test_add_book_in_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Машина времени')
        collector.add_book_in_favorites('Машина времени')

        assert 'Машина времени' in collector.favorites

    # добавление в избранное несуществующей книги
    def test_add_book_in_favorites_invalid(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Оно')

        assert 'Оно' not in collector.favorites

    # удаление книги из избранного
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Олле Лукойе')
        collector.add_book_in_favorites('Олле Лукойе')

        collector.delete_book_from_favorites('Олле Лукойе')
        assert 'Олле Лукойе' not in collector.favorites

    # получение списка избранного
    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book('Машина времени')
        collector.add_new_book('Сумерки')

        collector.add_book_in_favorites('Машина времени')
        collector.add_book_in_favorites('Сумерки')

        favorites = collector.get_list_of_favorites_books()
        assert len(favorites) == 2
        assert 'Машина времени' in favorites
        assert 'Сумерки' in favorites



