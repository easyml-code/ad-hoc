from collections import defaultdict

class BookStore:
    # main class to store all the books and their details, which is a dictionary
    def _init_(self) -> None:
        self.bookstore = dict()
    
    def _addBook(self, bookname, content):
        self.bookstore[bookname] = content
    
