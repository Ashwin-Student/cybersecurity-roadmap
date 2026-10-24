class LibraryBook:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_issued = False

    def issue_book(self):
        if self.is_issued == False:
            self.is_issued = True
            print("Book issued successfully")
        else:
            print("Book is currently unavailable")

    def return_book(self):
        self.is_issued = False
        print("Book returned successfully")


# Create a book object
book = LibraryBook("Python Programming", "John Smith")

# Issue the book
book.issue_book()

# Try to issue it again
book.issue_book()

# Return the book
book.return_book()