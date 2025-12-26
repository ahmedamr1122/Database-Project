import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../../context/AuthContext';

const SearchBooks = () => {
  const [searchParams, setSearchParams] = useState({
    query: '',
    category: '',
    author: '',
    publisher: ''
  });
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [addingToCart, setAddingToCart] = useState({});

  const { user } = useContext(AuthContext);

  useEffect(() => {
    // Load all books initially
    searchBooks();
  }, []);

  const handleSearchChange = (e) => {
    const { name, value } = e.target;
    setSearchParams(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const searchBooks = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const queryString = new URLSearchParams(searchParams).toString();
      const response = await fetch(`http://localhost:5000/books/search?${queryString}`);

      const data = await response.json();

      if (response.ok) {
        setBooks(data.books || []);
      } else {
        setError(data.error || 'Failed to search books');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const clearSearch = () => {
    setSearchParams({
      query: '',
      category: '',
      author: '',
      publisher: ''
    });
    searchBooks();
  };

  const addToCart = async (isbn) => {
    if (!user) {
      setError('Please login to add books to cart');
      return;
    }

    setAddingToCart(prev => ({ ...prev, [isbn]: true }));

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/customer/cart/add', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ isbn, quantity: 1 })
      });

      const data = await response.json();

      if (response.ok) {
        alert('Book added to cart successfully!');
      } else {
        setError(data.error || 'Failed to add to cart');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Add to cart error:', error);
    } finally {
      setAddingToCart(prev => ({ ...prev, [isbn]: false }));
    }
  };

  return (
    <div>
      <h2 className="mb-4">
        <i className="fas fa-search"></i> Search Books
      </h2>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {/* Search Form */}
      <div className="card mb-4">
        <div className="card-body">
          <form onSubmit={searchBooks}>
            <div className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="query" className="form-label">Search</label>
                <input
                  type="text"
                  className="form-control"
                  id="query"
                  name="query"
                  value={searchParams.query}
                  onChange={handleSearchChange}
                  placeholder="Title, ISBN, or author..."
                />
              </div>
              <div className="col-md-3 mb-3">
                <label htmlFor="category" className="form-label">Category</label>
                <select
                  className="form-select"
                  id="category"
                  name="category"
                  value={searchParams.category}
                  onChange={handleSearchChange}
                >
                  <option value="">All Categories</option>
                  <option value="Science">Science</option>
                  <option value="Art">Art</option>
                  <option value="Religion">Religion</option>
                  <option value="History">History</option>
                  <option value="Geography">Geography</option>
                </select>
              </div>
              <div className="col-md-3 mb-3">
                <label className="form-label">&nbsp;</label>
                <div className="d-flex gap-2">
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                        Searching...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-search"></i> Search
                      </>
                    )}
                  </button>
                  <button
                    type="button"
                    className="btn btn-outline-secondary"
                    onClick={clearSearch}
                  >
                    <i className="fas fa-times"></i> Clear
                  </button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>

      {/* Results */}
      {loading ? (
        <div className="text-center py-5">
          <div className="spinner-border" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      ) : books.length === 0 ? (
        <div className="text-center py-5">
          <i className="fas fa-book fa-4x text-muted mb-3"></i>
          <h4>No books found</h4>
          <p className="text-muted">Try adjusting your search criteria</p>
        </div>
      ) : (
        <div className="row">
          {books.map((book) => (
            <div key={book.isbn} className="col-md-6 col-lg-4 mb-4">
              <div className="card h-100">
                <div className="card-body d-flex flex-column">
                  <h5 className="card-title">{book.title}</h5>
                  <p className="card-text">
                    <strong>Author:</strong> {book.authors || 'Unknown'}<br />
                    <strong>Publisher:</strong> {book.publisher_name}<br />
                    <strong>Category:</strong> {book.category}<br />
                    <strong>Price:</strong> ${book.selling_price.toFixed(2)}<br />
                    <strong>Stock:</strong> {book.stock > 0 ? `${book.stock} available` : 'Out of stock'}
                  </p>
                  <div className="mt-auto">
                    <button
                      className="btn btn-primary w-100"
                      onClick={() => addToCart(book.isbn)}
                      disabled={!user || book.stock === 0 || addingToCart[book.isbn]}
                    >
                      {addingToCart[book.isbn] ? (
                        <>
                          <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                          Adding...
                        </>
                      ) : !user ? (
                        'Login to Add'
                      ) : book.stock === 0 ? (
                        'Out of Stock'
                      ) : (
                        <>
                          <i className="fas fa-cart-plus"></i> Add to Cart
                        </>
                      )}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default SearchBooks;
