from http.server import BaseHTTPRequestHandler, HTTPServer
import xml.etree.ElementTree as ET
import os
import json

DATA_FILE = "books.xml"

if not os.path.exists(DATA_FILE):
    root = ET.Element("books")
    tree = ET.ElementTree(root)
    tree.write(DATA_FILE)

class SimpleAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/books"):
            self.handle_get()
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        if self.path == "/books":
            self.handle_post()
        else:
            self.send_error(404, "Not Found")

    def do_PUT(self):
        if self.path.startswith("/books/"):
            self.handle_put()
        else:
            self.send_error(404, "Not Found")

    def do_DELETE(self):
        if self.path.startswith("/books/"):
            self.handle_delete()
        else:
            self.send_error(404, "Not Found")

    def handle_get(self):
        tree = ET.parse(DATA_FILE)
        root = tree.getroot()
        
        parts = self.path.split("/")
        if len(parts) > 2 and parts[2].isdigit():  # If URL has an ID
            book_id = parts[2]
            book = root.find(f".//book[@id='{book_id}']")
        
            if book is None:
                self.send_error(404, "Book not found")
                return
        
            book_data = {
                "id": book.get("id"),
                "title": book.find("title").text,
                "author": book.find("author").text
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(book_data).encode())

        else:  # If no ID, return all books
            books = []
            for book in root.findall("book"):
                books.append({
                    "id": book.get("id"),
                    "title": book.find("title").text,
                    "author": book.find("author").text
                })
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(books).encode())

    def handle_post(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length).decode().split(";")  # Expect "title;author"
        
        if len(data) != 2:
            self.send_error(400, "Invalid format. Expected: title;author")
            return
        
        title, author = data
        tree = ET.parse(DATA_FILE)
        root = tree.getroot()

        new_id = str(len(root) + 1)
        new_book = ET.SubElement(root, "book", id=new_id)
        ET.SubElement(new_book, "title").text = title
        ET.SubElement(new_book, "author").text = author

        tree.write(DATA_FILE)

        self.send_response(201)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"Book {new_id} created".encode())

    def handle_put(self):
        book_id = self.path.split("/")[-1]
        tree = ET.parse(DATA_FILE)
        root = tree.getroot()

        book = root.find(f".//book[@id='{book_id}']")
        if book is None:
            self.send_error(404, "Book not found")
            return

        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length).decode().split(";")  # Expect "title;author"

        if len(data) != 2:
            self.send_error(400, "Invalid format. Expected: title;author")
            return
        
        title, author = data
        book.find("title").text = title
        book.find("author").text = author
        tree.write(DATA_FILE)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"Book {book_id} updated".encode())

    def handle_delete(self):
        book_id = self.path.split("/")[-1]
        tree = ET.parse(DATA_FILE)
        root = tree.getroot()

        book = root.find(f".//book[@id='{book_id}']")
        if book is None:
            self.send_error(404, "Book not found")
            return

        root.remove(book)
        tree.write(DATA_FILE)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"Book {book_id} deleted".encode())


def run():
    server = HTTPServer(('localhost', 5000), SimpleAPI)
    print("Starting server on port 5000...")
    server.serve_forever()

if __name__ == "__main__":
    run()