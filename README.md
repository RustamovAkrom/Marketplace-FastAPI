# 🛒 Marketplace — Modern E‑Commerce Backend Platform

[url roadmap](https://roadmap.sh/projects/scalable-ecommerce-platform)

**Marketplace** is a high‑performance, scalable, and modular e‑commerce backend built with **FastAPI**. It provides a fully structured architecture that covers every essential part of an online marketplace: user authentication, product catalog, carts, orders, delivery logistics, image upload system, and review management.

Designed following **clean architecture principles**, the project is maintainable, extendable, and production‑ready.

## 🚀 Features

### 👤 Users & Authentication

* User registration & login
* Logout and token revocation
* Refresh token workflow
* Password recovery via email
* Secure JWT‑based authentication (access + refresh tokens)
* Role system with permissions:

  * **Buyer**
  * **Seller**
  * **Courier**
  * **Admin**

---

## 🔐 Security

* Password hashing with **bcrypt**
* Revoked token tracking (logout / logout_all)
* Role‑based access control
* Strict Pydantic validation for all input/output data
* Secure and isolated file upload handling

---

## 💾 Tech Stack

| Layer                  | Technologies                             |
| ---------------------- | ---------------------------------------- |
| **Backend**            | FastAPI, SQLAlchemy 2.0, Alembic         |
| **Database**           | PostgreSQL                               |
| **Async**              | asyncpg, aiofiles                        |
| **Authentication**     | OAuth2, JWT (Access & Refresh)           |
| **Caching (optional)** | Redis                                    |
| **File Storage**       | `/media` directory with hashed filenames |
| **Testing**            | Pytest                                   |
| **DevOps (optional)**  | GitHub Actions                           |

---

## 🗄️ Database SQL Diagram

![](/docs/media/diagram.png)

> Project SQL diagram overview

### Core Tables

* **users**
* **sellers**
* **couriers**
* **delivery_addresses**
* **deliveries**
* **product_variants**
* **products**
* **product_images**
* **orders**
* **order_items**
* **brands**
* **categories**
* **carts**
* **cart_items**
* **promo_codes**

---

## 📂 Project Structure

```bash
src/
 ├── api/
 │   └── v1/
 │       ├── auth/
 │       ├── users/
 │       ├── products/
 │       ├── categories/
 │       ├── seller/
 │       ├── courier/
 │       ├── orders/
 │       └── delivery/
 ├── core/
 │   ├── config.py
 │   └── security.py
 ├── db/
 │   ├── session.py
 │   ├── base.py
 │   └── models/
 │       ├── users.py
 │       ├── products.py
 │       ├── categories.py
 │       ├── brands.py
 │       ├── cart.py
 │       ├── orders.py
 │       ├── delivery.py
 │       ├── seller_profile.py
 │       ├── courier_profile.py
 │       └── review.py
 ├── services/
 └── media/
```

---

## 🧠 Architecture

### ✔ Clean Architecture

* Clear separation between API, services, repositories, and database models
* Easy to extend and maintain

### ✔ Modular & Scalable

* Each domain (products, orders, delivery, etc.) is fully isolated
* Can be easily split into microservices (catalog, delivery, payments, etc.)

### ✔ Async‑first Design

* High throughput thanks to async stack
* Perfect for real‑time tasks such as courier tracking

---



## ▶️ Getting Started (Without Docker)

### 1. Clone Repository

```bash
git clone https://github.com/RustamovAkrom/Marketplace-FastAPI.git
cd Marketplace-FastAPI
```

### 2. Create `.env` File

```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
SECRET_KEY=your-secret-key
DEBUG=true
```

### 3. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Start Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Open API Docs

```
http://localhost:8000/docs
```

---

## 🧪 Tests

Run all tests using:

```bash
pytest -vv
```

---

## 👨‍💻 Author

**Akrom** — Backend developer passionate about scalable architecture, clean code, and modern engineering practices. Building a production‑ready e‑commerce backend for real-world use and portfolio purposes.

---

## 📄 License

MIT License
