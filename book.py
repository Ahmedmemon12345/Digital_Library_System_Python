import streamlit as st

# ------------------ CLASSES ------------------

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
        if not book.title or not book.author or not book.book_id:
            return False, "❌ All fields are required!"

        if book.book_id in self.books:
            return False, "❌ Book ID already exists!"

        self.books[book.book_id] = book
        return True, "✅ Books added successfully!"

    def search_by_title(self, title):
        return [b for b in self.books.values() if title.lower() in b.title.lower()]

    def search_by_author(self, author):
        return [b for b in self.books.values() if author.lower() in b.author.lower()]

    def borrow_book(self, user, book_id):
        if not user or not book_id:
            return False, "❌ All fields are required!"

        if book_id not in self.books:
            return False, "❌ Invalid Book ID!"

        if (user, book_id) in self.borrow_records:
            return False, "❌ You already borrowed this book!"

        book = self.books[book_id]
        if book.available_copies == 0:
            return False, "❌ No copies available!"

        book.available_copies -= 1
        self.borrow_records.append((user, book_id))
        return True, f"✅ {user} borrowed {book.title}"

    def return_book(self, user, book_id):
        if not user or not book_id:
            return False, "❌ All fields are required!"

        if book_id not in self.books:
            return False, "❌ Invalid Book ID!"

        if (user, book_id) not in self.borrow_records:
            return False, "❌ This user did not borrow this book."

        book = self.books[book_id]
        book.available_copies += 1
        self.borrow_records.remove((user, book_id))
        return True, f"✅ {user} returned {book.title}"


# ------------------ SESSION STATE ------------------

if "library" not in st.session_state:
    st.session_state.library = Library()

library = st.session_state.library

# ------------------ STREAMLIT UI ------------------

st.title("📚 Digital Library System")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Add Book",
        "Search by Title",
        "Search by Author",
        "Borrow Book",
        "Return Book",
        "View All Books",
        "Borrow Records",
    ],
)

# ------------------ ADD BOOK ------------------

if menu == "Add Book":
    st.header("➕ Add Book")

    title = st.text_input("Book Title")
    author = st.text_input("Author")
    book_id = st.text_input("Book ID")
    copies = st.number_input("Total Copies", min_value=1, step=1)

    if st.button("Add Book"):
        success, msg = library.add_book(Book(title, author, book_id, copies))
        st.success(msg)

# ------------------ SEARCH BY TITLE ------------------

elif menu == "Search by Title":
    st.header("🔍 Search Book by Title")

    title = st.text_input("Enter Title")
    if st.button("Search"):
        results = library.search_by_title(title)
        if results:
            for b in results:
                st.write(f"📘 {b.title} | {b.author} | Available: {b.available_copies}")
        else:
            st.warning("No books found")

# ------------------ SEARCH BY AUTHOR ------------------

elif menu == "Search by Author":
    st.header("🖊 Search Book by Author")

    author = st.text_input("Enter Author Name")
    if st.button("Search"):
        results = library.search_by_author(author)
        if results:
            for b in results:
                st.write(f"📘 {b.title} | {b.author} | Available: {b.available_copies}")
        else:
            st.warning("No books found")

# ------------------ BORROW BOOK ------------------

elif menu == "Borrow Book":
    st.header("📥 Borrow Book")

    user = st.text_input("Your Name")
    book_id = st.text_input("Book ID")

    if st.button("Borrow"):
        success, msg = library.borrow_book(user, book_id)
        st.success(msg)

# ------------------ RETURN BOOK ------------------

elif menu == "Return Book":
    st.header("📤 Return Book")

    user = st.text_input("Your Name")
    book_id = st.text_input("Book ID")

    if st.button("Return"):
        success, msg = library.return_book(user, book_id)
        st.success(msg)

# ------------------ VIEW ALL BOOKS ------------------

elif menu == "View All Books":
    st.header("📚 All Books")

    if library.books:
        for b in library.books.values():
            st.write(
                f"📘 {b.title} | {b.author} | "
                f"Total: {b.total_copies} | Available: {b.available_copies}"
            )
    else:
        st.warning("No books added")

# ------------------ BORROW RECORDS ------------------

elif menu == "Borrow Records":
    st.header("📄 Borrowed Book Records")

    if library.borrow_records:
        for user, book_id in library.borrow_records:
            book = library.books[book_id]
            st.write(f"➡️ {user} borrowed {book.title}")
    else:
        st.warning("No borrow records found")
