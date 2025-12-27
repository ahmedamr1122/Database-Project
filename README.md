# 📚 Online Bookstore

A full-stack web application for an online bookstore built with Flask and MySQL.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)

## ✨ Features

### Customer Features

- 🔍 Search books by ISBN, title, author, publisher, or category
- 🛒 Shopping cart with quantity management
- 💳 Secure checkout with credit card validation
- 📦 Order history tracking
- 👤 Profile management

### Admin Features

- 📊 Dashboard with live statistics
- 📚 Add, modify, and manage books
- 🏢 Manage publishers
- 📈 Generate sales reports
- 📋 View and confirm publisher orders
- ⚠️ Low stock alerts with auto-reorder system

## 🛠️ Tech Stack

| Layer          | Technology              |
| -------------- | ----------------------- |
| Backend        | Python Flask            |
| Database       | MySQL 8.0               |
| Frontend       | HTML5, CSS3, JavaScript |
| UI Framework   | Bootstrap 5             |
| Authentication | bcrypt                  |
| Container      | Docker                  |

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Docker & Docker Compose

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/Database-Project.git
   cd Database-Project
   ```

2. **Start the database**

   ```bash
   docker compose up -d
   ```

3. **Install dependencies**

   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Initialize the database**

   ```bash
   docker exec -i bookstore_db mysql -u root -proot OnlineBookstore < backend/database/db.sql
   docker exec -i bookstore_db mysql -u root -proot OnlineBookstore < backend/database/seed_data.sql
   ```

5. **Run the application**

   ```bash
   cd backend
   python3 -m app
   ```

6. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🔐 Test Accounts

| Role         | Username       | Password      |
| ------------ | -------------- | ------------- |
| Admin        | `admin`        | `password123` |
| Customer     | `john_doe`     | `password123` |
| VIP Customer | `vip_customer` | `password123` |

## 📁 Project Structure

```
├── backend/
│   ├── app.py              # Application entry
│   ├── database/           # SQL schemas
│   ├── models/             # Business logic
│   ├── routes/             # API endpoints
│   └── utils/              # Helpers
├── frontend/
│   ├── templates/          # HTML views
│   └── static/             # CSS, JS, images
└── docker-compose.yml
```

## 📊 Database Features

- **Triggers**: Automatic stock management & publisher reorder
- **Transactions**: ACID-compliant order processing
- **Relationships**: Proper normalization with foreign keys

## 📄 License

This project is part of a Database Systems course at Alexandria University.

## 👥 Team

- Database Design & Backend Development
- Frontend Integration & Testing
