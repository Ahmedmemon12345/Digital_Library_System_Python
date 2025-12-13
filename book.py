import streamlit as st

class Book:
    def __init__(self, title, author, book_id, total_copies):
        self.title = title
        self.author = author
        self.book_id = book_id
        self.total_copies = total_copies
        self.available_copies = total_copies

class Library:
    def __init__(self):
        self.books = {}
        self.borrow_records = []

    def add_book(self, book):
        if book.book_id in self.books:
            return "Book ID already exists!"
        self.books[book.book_id] = book
        return "Book added successfully!"

    def search_by_title(self, title):
        return [b for b in self.books.values() if title.lower() in b.title.lower()]

    def search_by_author(self, author):
        return [b for b in self.books.values() if author.lower() in b.author.lower()]

    def borrow_book(self, user, book_id):
        if book_id not in self.books:
            return "Invalid Book ID!"
        book = self.books[book_id]
        if book.available_copies == 0:
            return "No copies available!"
        book.available_copies -= 1
        self.borrow_records.append((user, book_id))
        return f"{user} borrowed {book.title}"

    def return_book(self, user, book_id):
        if (user, book_id) not in self.borrow_records:
            return "This user did not borrow this book."
        book = self.books[book_id]
        book.available_copies += 1
        self.borrow_records.remove((user, book_id))
        return f"{user} returned {book.title}"

# -------------------------- STREAMLIT UI --------------------------
library = Library()

st.title("📚 Digital Library System (Streamlit Version)")

menu = st.sidebar.selectbox(
    "Menu",
    ["Add Book", "Search by Title", "Search by Author",
     "Borrow Book", "Return Book", "View All Books", "Borrow Records"]
)

# Add Book
if menu == "Add Book":
    st.header("➕ Add Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    book_id = st.text_input("Book ID")
    copies = st.number_input("Total Copies", min_value=1)

    if st.button("Add"):
        msg = library.add_book(Book(title, author, book_id, copies))
        st.success(msg)

# Search by Title
elif menu == "Search by Title":
    st.header("🔍 Search Book by Title")
    title = st.text_input("Enter Title")
    if st.button("Search"):
        results = library.search_by_title(title)
        for b in results:
            st.write(f"📘 {b.title} | {b.author} | Available: {b.available_copies}")

# Search by Author
elif menu == "Search by Author":
    st.header("🖊 Search Book by Author")
    author = st.text_input("Enter Author Name")
    if st.button("Search"):
        results = library.search_by_author(author)
        for b in results:
            st.write(f"📘 {b.title} | {b.author} | Available: {b.available_copies}")

# Borrow Book
elif menu == "Borrow Book":
    st.header("📥 Borrow Book")
    user = st.text_input("Your Name")
    book_id = st.text_input("Book ID")
    if st.button("Borrow"):
        msg = library.borrow_book(user, book_id)
        st.success(msg)

# Return Book
elif menu == "Return Book":
    st.header("📤 Return Book")
    user = st.text_input("Your Name")
    book_id = st.text_input("Book ID")
    if st.button("Return"):
        msg = library.return_book(user, book_id)
        st.success(msg)

# View All Books
elif menu == "View All Books":
    st.header("📚 All Books")
    for b in library.books.values():
        st.write(f"📘 {b.title} | {b.author} | Total: {b.total_copies} | Available: {b.available_copies}")

# Borrow Records
elif menu == "Borrow Records":
    st.header("📄 Borrowed Book Records")
    for user, book_id in library.borrow_records:
        book = library.books[book_id]
        st.write(f"➡️ {user} borrowed {book.title}")
