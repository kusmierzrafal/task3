import unittest
from project.books.models import Book


class TestBookModel(unittest.TestCase):
    
    # Testy poprawnych danych
    def test_valid_book_creation(self):
        book = Book("Valid Book", "Valid Author", 2020, "fiction")
        self.assertEqual(book.name, "Valid Book")
        self.assertEqual(book.author, "Valid Author")
        self.assertEqual(book.year_published, 2020)
        self.assertEqual(book.book_type, "fiction")
        self.assertEqual(book.status, "available")

    def test_book_with_custom_status(self):
        book = Book("Test Book", "Test Author", 2021, "non-fiction", "borrowed")
        self.assertEqual(book.status, "borrowed")

    # Testy niepoprawnych danych
    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Book("", "Author", 2020, "fiction")

    def test_empty_author(self):
        with self.assertRaises(ValueError):
            Book("Book", "", 2020, "fiction")

    def test_negative_year(self):
        with self.assertRaises(ValueError):
            Book("Book", "Author", -100, "fiction")

    def test_string_year_invalid(self):
        with self.assertRaises(ValueError):
            Book("Book", "Author", "notayear", "fiction")

    # Testy SQL Injection
    def test_sql_injection_name(self):
        malicious_name = "'; DROP TABLE books; --"
        with self.assertRaises(ValueError):
            Book(malicious_name, "Author", 2020, "fiction")

    def test_sql_injection_author(self):
        malicious_author = "Robert'; DELETE FROM books WHERE 1=1; --"
        with self.assertRaises(ValueError):
            Book("Book", malicious_author, 2020, "fiction")

    def test_sql_injection_book_type(self):
        malicious_type = "fiction'; UPDATE books SET status='stolen'; --"
        with self.assertRaises(ValueError):
            Book("Book", "Author", 2020, malicious_type)

    def test_sql_injection_status(self):
        malicious_status = "available'; DROP DATABASE library; --"
        with self.assertRaises(ValueError):
            Book("Book", "Author", 2020, "fiction", malicious_status)

    # Testy JavaScript Injection
    def test_javascript_injection_name(self):
        js_name = "<script>alert('XSS')</script>"
        with self.assertRaises(ValueError):
            Book(js_name, "Author", 2020, "fiction")

    def test_javascript_injection_author(self):
        js_author = "javascript:alert('XSS')"
        with self.assertRaises(ValueError):
            Book("Book", js_author, 2020, "fiction")

    def test_javascript_injection_book_type(self):
        js_type = "<script>alert('XSS')</script>"
        with self.assertRaises(ValueError):
            Book("Book", "Author", 2020, js_type)

    def test_javascript_injection_status(self):
        js_status = "<img src=x onerror=alert('XSS')>"
        with self.assertRaises(ValueError):
            Book("Book", "Author", 2020, "fiction", js_status)

    # Testy ekstremalne
    def test_extreme_name_too_long(self):
        extreme_name = "A" * 1000
        with self.assertRaises(ValueError):
            Book(extreme_name, "Author", 2020, "fiction")

    def test_extreme_author_too_long(self):
        extreme_author = "B" * 1000
        with self.assertRaises(ValueError):
            Book("Book", extreme_author, 2020, "fiction")

    def test_extreme_year_too_high(self):
        with self.assertRaises(ValueError):
            Book("Book", "Author", 9999, "fiction")

    def test_extreme_year_too_low(self):
        with self.assertRaises(ValueError):
            Book("Book", "Author", -1000, "fiction")

    def test_extreme_book_type_too_long(self):
        extreme_type = "C" * 1000
        with self.assertRaises(ValueError):
            Book("Book", "Author", 2020, extreme_type)

    def test_extreme_status_too_long(self):
        extreme_status = "D" * 1000
        with self.assertRaises(ValueError):
            Book("Book", "Author", 2020, "fiction", extreme_status)

    def test_float_year_conversion(self):
        with self.assertRaises(ValueError):
            Book("Book", "Author", 2020.5, "fiction")

    def test_string_year(self):
        with self.assertRaises(ValueError):
            Book("Book", "Author", "invalid_year", "fiction")

    def test_boolean_values(self):
        with self.assertRaises(ValueError):
            Book(True, False, True, False)


if __name__ == '__main__':
    unittest.main()
