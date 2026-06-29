def _ru_plural(n, one, few, many):
    n = abs(int(n))
    if 11 <= n % 100 <= 14:
        return many
    remainder = n % 10
    if remainder == 1:
        return one
    if 2 <= remainder <= 4:
        return few
    return many


def format_books_on_shelves(book_count, shelf_count):
    books_word = _ru_plural(book_count, "книга", "книги", "книг")
    shelves_word = _ru_plural(shelf_count, "полке", "полках", "полках")
    return f"{book_count} {books_word} на {shelf_count} {shelves_word}"
