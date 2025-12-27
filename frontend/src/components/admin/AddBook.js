import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../../context/AuthContext';

const AddBook = () => {
  const [formData, setFormData] = useState({
    isbn: '',
    title: '',
    publisher_name: '',
    pub_year: '',
    selling_price: '',
    category: 'Science',
    stock: 0,
    threshold: 10,
    authors: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const { user } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const token = localStorage.getItem('token');

      // Prepare data
      const bookData = {
        ...formData,
        pub_year: formData.pub_year ? parseInt(formData.pub_year) : null,
        selling_price: parseFloat(formData.selling_price),
        stock: parseInt(formData.stock),
        threshold: parseInt(formData.threshold),
        authors: formData.authors.split(',').map(author => author.trim())
      };

      const response = await fetch('http://localhost:5000/admin/books', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(bookData)
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess('Book added successfully!');
        // Reset form
        setFormData({
          isbn: '',
          title: '',
          publisher_name: '',
          pub_year: '',
          selling_price: '',
          category: 'Science',
          stock: 0,
          threshold: 10,
          authors: ''
        });
      } else {
        setError(data.error || 'Failed to add book');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Add book error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2 className="mb-4">
        <i className="fas fa-plus-circle"></i> Add New Book
      </h2>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      {success && (
        <div className="alert alert-success" role="alert">
          {success}
        </div>
      )}

      <div className="card">
        <div className="card-body">
          <form onSubmit={handleSubmit}>
            <div className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="isbn" className="form-label">ISBN *</label>
                <input
                  type="text"
                  className="form-control"
                  id="isbn"
                  name="isbn"
                  value={formData.isbn}
                  onChange={handleChange}
                  required
                  placeholder="978-0-123456-78-9"
                />
              </div>
              <div className="col-md-6 mb-3">
                <label htmlFor="title" className="form-label">Title *</label>
                <input
                  type="text"
                  className="form-control"
                  id="title"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="publisher_name" className="form-label">Publisher *</label>
                <input
                  type="text"
                  className="form-control"
                  id="publisher_name"
                  name="publisher_name"
                  value={formData.publisher_name}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="col-md-6 mb-3">
                <label htmlFor="pub_year" className="form-label">Publication Year</label>
                <input
                  type="number"
                  className="form-control"
                  id="pub_year"
                  name="pub_year"
                  value={formData.pub_year}
                  onChange={handleChange}
                  min="1000"
                  max={new Date().getFullYear()}
                />
              </div>
            </div>

            <div className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="selling_price" className="form-label">Selling Price *</label>
                <div className="input-group">
                  <span className="input-group-text">$</span>
                  <input
                    type="number"
                    className="form-control"
                    id="selling_price"
                    name="selling_price"
                    value={formData.selling_price}
                    onChange={handleChange}
                    step="0.01"
                    min="0"
                    required
                  />
                </div>
              </div>
              <div className="col-md-6 mb-3">
                <label htmlFor="category" className="form-label">Category *</label>
                <select
                  className="form-select"
                  id="category"
                  name="category"
                  value={formData.category}
                  onChange={handleChange}
                  required
                >
                  <option value="Science">Science</option>
                  <option value="Art">Art</option>
                  <option value="Religion">Religion</option>
                  <option value="History">History</option>
                  <option value="Geography">Geography</option>
                </select>
              </div>
            </div>

            <div className="row">
              <div className="col-md-6 mb-3">
                <label htmlFor="stock" className="form-label">Initial Stock</label>
                <input
                  type="number"
                  className="form-control"
                  id="stock"
                  name="stock"
                  value={formData.stock}
                  onChange={handleChange}
                  min="0"
                />
              </div>
              <div className="col-md-6 mb-3">
                <label htmlFor="threshold" className="form-label">Stock Threshold</label>
                <input
                  type="number"
                  className="form-control"
                  id="threshold"
                  name="threshold"
                  value={formData.threshold}
                  onChange={handleChange}
                  min="0"
                />
              </div>
            </div>

            <div className="mb-3">
              <label htmlFor="authors" className="form-label">Authors</label>
              <input
                type="text"
                className="form-control"
                id="authors"
                name="authors"
                value={formData.authors}
                onChange={handleChange}
                placeholder="Author 1, Author 2, Author 3"
              />
              <div className="form-text">Separate multiple authors with commas</div>
            </div>

            <div className="d-flex gap-2">
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <span className="spinner-border spinner-border-sm me-2"></span>
                    Adding Book...
                  </>
                ) : (
                  <>
                    <i className="fas fa-plus-circle"></i> Add Book
                  </>
                )}
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => navigate('/admin/dashboard')}
              >
                <i className="fas fa-arrow-left"></i> Back to Dashboard
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AddBook;
