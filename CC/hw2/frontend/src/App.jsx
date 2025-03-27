import React, { useState } from "react";

function App() {
  const [books, setBooks] = useState([]);
  const [title, setTitle] = useState("");
  const [author, setAuthor] = useState("");
  const [bookId, setBookId] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [singleBook, setSingleBook] = useState(null); 
  const [bookSummary, setBookSummary] = useState("");
  const [weatherData, setWeatherData] = useState(null);
  const [city, setCity] = useState("London");

const fetchWeather = async () => {
  setError("");
  setSuccess("");
  setWeatherData(null);

  try {
    const response = await fetch(`http://localhost:8000/weather?city=${city}`);
    if (!response.ok) throw new Error("Failed to fetch weather data.");
    const data = await response.json();
    setWeatherData(data);
    setSuccess(`Fetched weather for ${data.city} successfully! ✅`);
  } catch (err) {
    setError("Error fetching weather: " + err.message);
  }
};


  const fetchBooks = async () => {
    setError("");
    setSuccess("");
    setSingleBook(null);
    try {
      const response = await fetch("http://localhost:8000/books");
      if (!response.ok) throw new Error("Failed to fetch books.");
      const data = await response.json();
      setBooks(data);
      setSuccess("Fetched all books successfully! ✅");
    } catch (err) {
      setError("Error fetching books: " + err.message);
    }
  };

  const fetchBookById = async () => {
    if (!bookId.trim()) {
      setError("Book ID cannot be empty.");
      return;
    }

    setError("");
    setSuccess("");
    setSingleBook(null);

    try {
      const response = await fetch(`http://localhost:8000/books/${bookId}`);
      if (response.status === 404) {
        setError(`Book ID [${bookId}] not found.`);
        return;
      }

      if (!response.ok) throw new Error("Failed to fetch book.");

      const data = await response.json();
      setSingleBook(data);
      setSuccess(`Book ID [${bookId}] fetched successfully! ✅`);
    } catch (err) {
      setError("Error fetching book: " + err.message);
    }
  };

  const addBook = async () => {
    if (!title.trim() || !author.trim()) {
      setError("Title and author cannot be empty.");
      return;
    }

    setError("");
    setSuccess("");

    try {
      const response = await fetch("http://localhost:8000/books", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, author }),
      });

      if (!response.ok) throw new Error("Failed to add book.");

      setSuccess("Book added successfully! ✅");
    // fetchBooks();
      setTitle(""); 
      setAuthor("");
    } catch (err) {
      setError("Error adding book: " + err.message);
    }
  };

  const updateBook = async () => {
    if (!bookId.trim() || !title.trim() || !author.trim()) {
      setError("Book ID, title, and author cannot be empty.");
      return;
    }

    setError("");
    setSuccess("");

    try {
      const response = await fetch(`http://localhost:8000/books/${bookId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, author }),
      });

      if (response.status === 404) {
        setError(`Book ID [${bookId}] doesn't exist.`);
        return;
      }

      if (!response.ok) throw new Error("Failed to update book.");

      setSuccess(`Book ID [${bookId}] updated successfully! ✅`);
      //fetchBooks();
      setBookId(""); 
      setTitle("");
      setAuthor("");
    } catch (err) {
      setError("Error updating book: " + err.message);
    }
  };

  const deleteBook = async () => {
    if (!bookId.trim()) {
      setError("Book ID cannot be empty.");
      return;
    }

    setError("");
    setSuccess("");

    try {
      const response = await fetch(`http://localhost:8000/books/${bookId}`, { method: "DELETE" });

      if (response.status === 404) {
        setError(`Book ID [${bookId}] doesn't exist.`);
        return;
      }

      if (!response.ok) throw new Error("Failed to delete book.");

      setSuccess(`Book ID [${bookId}] deleted successfully! ✅`);
      //fetchBooks();
      setBookId("");
    } catch (err) {
      setError("Error deleting book: " + err.message);
    }
  };

  const deleteAllBooks = async () => {
    setError("");
    setSuccess("");

    try {
      const response = await fetch("http://localhost:8000/books", { method: "DELETE" });

      if (!response.ok) throw new Error("Failed to delete all books.");

      setSuccess("All books deleted successfully! ✅");
      //fetchBooks();
    } catch (err) {
      setError("Error deleting all books: " + err.message);
    }
  };

  const fetchBookInfo = async () => {
    if (!bookId.trim()) {
      setError("Book ID cannot be empty.");
      return;
    }

    setError("");
    setSuccess("");
    setBookSummary("");

    try {
      const response = await fetch(`http://localhost:8000/book-info/${bookId}`);
      if (response.status === 404) {
        setError(`Book ID [${bookId}] not found.`);
        return;
      }

      if (!response.ok) throw new Error("Failed to fetch book info.");

      const data = await response.json();
      setBookSummary(data.summary);
      setSuccess(`Fetched Wikipedia summary for "${data.title}" ✅`);
    } catch (err) {
      setError("Error fetching book info: " + err.message);
    }
  };

  return (
    <div>
      <h1>Book Management</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}

      <button onClick={fetchBooks}>Get Books</button>
      <button onClick={deleteAllBooks} style={{ marginLeft: "10px", backgroundColor: "red", color: "white" }}>Delete All Books</button>

      <div>
        <input
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          placeholder="Author"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
        />
        <button onClick={addBook}>Add Book</button>
      </div>

      <div>
        <input
          placeholder="Book ID"
          value={bookId}
          onChange={(e) => setBookId(e.target.value)}
        />
        <button onClick={fetchBookById}>Get Book</button>
        <button onClick={updateBook}>Update Book</button>
        <button onClick={deleteBook}>Delete Book</button>
        <button onClick={fetchBookInfo} style={{ backgroundColor: "lightblue" }}>Book Info</button> {}
      </div>

      {singleBook && (
        <div>
          <h2>Single Book Details</h2>
          <p><strong>ID:</strong> {singleBook.id}</p>
          <p><strong>Title:</strong> {singleBook.title}</p>
          <p><strong>Author:</strong> {singleBook.author}</p>
        </div>
      )}

      {bookSummary && (
        <div>
          <h2>Book Summary (Wikipedia)</h2>
          <p>{bookSummary}</p>
        </div>
      )}

      <h2>Books List</h2>
      <ul>
        {books.map((book) => (
          <li key={book.id}>
            <strong>ID:</strong> {book.id} | <strong>Title:</strong> {book.title} | <strong>Author:</strong> {book.author}
          </li>
        ))}
      </ul>

      <h1>Weather</h1>
      <div>
  <input
    placeholder="City"
    value={city}
    onChange={(e) => setCity(e.target.value)}
  />
  <button onClick={fetchWeather} style={{ backgroundColor: "orange" }}>Show Weather</button>
</div>

{weatherData && (
  <div>
    <h2>Weather in {weatherData.city}</h2>
    <p><strong>Temperature:</strong> {weatherData.temperature}°C</p>
    <p><strong>Description:</strong> {weatherData.description}</p>
  </div>
)}

    </div>
    
  );
}

export default App;