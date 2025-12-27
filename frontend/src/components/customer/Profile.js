import React, { useState, useEffect, useContext } from 'react';
import AuthContext from '../../context/AuthContext';

const Profile = () => {
  const [profileData, setProfileData] = useState({
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    phone_number: '',
    shipping_address: ''
  });
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_new_password: ''
  });
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const { user } = useContext(AuthContext);

  useEffect(() => {
    if (user) {
      fetchProfile();
    }
  }, [user]);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/customer/profile', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (response.ok) {
        setProfileData(data.user || {});
      } else {
        setError(data.error || 'Failed to load profile');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Profile fetch error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const updateProfile = async (e) => {
    e.preventDefault();
    setUpdating(true);
    setError('');
    setSuccess('');

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/customer/profile', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(profileData)
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess('Profile updated successfully!');
        // Update local storage
        const updatedUser = { ...user, ...profileData };
        localStorage.setItem('user', JSON.stringify(updatedUser));
      } else {
        setError(data.error || 'Failed to update profile');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Profile update error:', error);
    } finally {
      setUpdating(false);
    }
  };

  const updatePassword = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (passwordData.new_password !== passwordData.confirm_new_password) {
      setError('New passwords do not match');
      return;
    }

    if (passwordData.new_password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setUpdating(true);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5000/customer/profile/password', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          current_password: passwordData.current_password,
          new_password: passwordData.new_password
        })
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess('Password updated successfully!');
        setPasswordData({
          current_password: '',
          new_password: '',
          confirm_new_password: ''
        });
      } else {
        setError(data.error || 'Failed to update password');
      }
    } catch (error) {
      setError('Network error. Please try again.');
      console.error('Password update error:', error);
    } finally {
      setUpdating(false);
    }
  };

  if (!user) {
    return (
      <div className="text-center py-5">
        <h3>Please login to view your profile</h3>
        <a href="/login" className="btn btn-primary">Login</a>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h2 className="mb-4">
        <i className="fas fa-user"></i> My Profile
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

      <div className="row">
        <div className="col-md-8">
          {/* Profile Information */}
          <div className="card mb-4">
            <div className="card-header">
              <h5 className="mb-0">Personal Information</h5>
            </div>
            <div className="card-body">
              <form onSubmit={updateProfile}>
                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="first_name" className="form-label">First Name</label>
                    <input
                      type="text"
                      className="form-control"
                      id="first_name"
                      name="first_name"
                      value={profileData.first_name}
                      onChange={handleProfileChange}
                      required
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <label htmlFor="last_name" className="form-label">Last Name</label>
                    <input
                      type="text"
                      className="form-control"
                      id="last_name"
                      name="last_name"
                      value={profileData.last_name}
                      onChange={handleProfileChange}
                      required
                    />
                  </div>
                </div>

                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="username" className="form-label">Username</label>
                    <input
                      type="text"
                      className="form-control"
                      id="username"
                      name="username"
                      value={profileData.username}
                      onChange={handleProfileChange}
                      required
                    />
                  </div>
                  <div className="col-md-6 mb-3">
                    <label htmlFor="email" className="form-label">Email</label>
                    <input
                      type="email"
                      className="form-control"
                      id="email"
                      name="email"
                      value={profileData.email}
                      onChange={handleProfileChange}
                      required
                    />
                  </div>
                </div>

                <div className="row">
                  <div className="col-md-6 mb-3">
                    <label htmlFor="phone_number" className="form-label">Phone Number</label>
                    <input
                      type="tel"
                      className="form-control"
                      id="phone_number"
                      name="phone_number"
                      value={profileData.phone_number}
                      onChange={handleProfileChange}
                    />
                  </div>
                </div>

                <div className="mb-3">
                  <label htmlFor="shipping_address" className="form-label">Shipping Address</label>
                  <textarea
                    className="form-control"
                    id="shipping_address"
                    name="shipping_address"
                    value={profileData.shipping_address}
                    onChange={handleProfileChange}
                    rows="3"
                  />
                </div>

                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={updating}
                >
                  {updating ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                      Updating...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-save"></i> Update Profile
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Change Password */}
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Change Password</h5>
            </div>
            <div className="card-body">
              <form onSubmit={updatePassword}>
                <div className="mb-3">
                  <label htmlFor="current_password" className="form-label">Current Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="current_password"
                    name="current_password"
                    value={passwordData.current_password}
                    onChange={handlePasswordChange}
                    required
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="new_password" className="form-label">New Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="new_password"
                    name="new_password"
                    value={passwordData.new_password}
                    onChange={handlePasswordChange}
                    required
                    minLength="6"
                  />
                </div>
                <div className="mb-3">
                  <label htmlFor="confirm_new_password" className="form-label">Confirm New Password</label>
                  <input
                    type="password"
                    className="form-control"
                    id="confirm_new_password"
                    name="confirm_new_password"
                    value={passwordData.confirm_new_password}
                    onChange={handlePasswordChange}
                    required
                    minLength="6"
                  />
                </div>
                <button
                  type="submit"
                  className="btn btn-warning"
                  disabled={updating}
                >
                  {updating ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                      Updating...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-key"></i> Change Password
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          {/* Profile Stats */}
          <div className="card">
            <div className="card-header">
              <h5 className="mb-0">Account Statistics</h5>
            </div>
            <div className="card-body">
              <div className="text-center">
                <i className="fas fa-user-circle fa-4x text-primary mb-3"></i>
                <h6>{profileData.first_name} {profileData.last_name}</h6>
                <p className="text-muted">{profileData.username}</p>
                <hr />
                <div className="row text-center">
                  <div className="col-6">
                    <h4 className="text-primary">5</h4>
                    <small className="text-muted">Total Orders</small>
                  </div>
                  <div className="col-6">
                    <h4 className="text-success">$500</h4>
                    <small className="text-muted">Total Spent</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
