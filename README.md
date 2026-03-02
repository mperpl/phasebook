# High-Performance FastAPI Social Media API
> **Early Development**. Core Auth & Session management functional. Social features in progress.

An asynchronous backend service built in **Python 3.12**. This project focuses on scalability and efficient session management using **FastAPI**, **SQLAlchemy**, and **Redis**.

## 🚀 Technical Highlights

### 🔐 Hybrid Session Management
Unlike standard stateless JWT implementations, this project uses a **Stateful Hybrid Approach**:
* **Client-Side**: Signed session cookies via `SessionMiddleware` for secure transport.
* **Server-Side**: Session tracking in **Redis**.
* **Benefit**: Allows for absolute control over user sessions, including **instant logout from all devices** and protection against stale session hijacking, which is a common limitation of pure JWT.

### ⚡ Performance Optimization (Caching Strategy)
* **Redis Hash Caching**: User profiles and frequently accessed metadata are stored as Redis Hashes. This avoids expensive PostgreSQL joins and reduces JSON serialization overhead.
* **Cache Invalidation**: Implements "write-through" or "stale-on-update" logic where the Redis cache is automatically updated or purged when user data changes (e.g., bio updates, username changes).

### 🔗 OAuth2 Flow
* Supports **Google, GitHub, and Facebook** social logins for good user experience.

### 🛠 Security & Reliability
* **Rate Limiting**: Integrated `slowapi` to mitigate brute-force attacks on sensitive endpoints (`/login`, `/register`).
* **Background Tasks**: Non-blocking email delivery for account verification using `FastAPI-Mail` and `BackgroundTasks`.
* **Data Integrity**: Strict validation using **Pydantic v2** and type-safety with Python's latest type hinting.

## 🛠 Tech Stack

* **Framework**: FastAPI
* **Database**: PostgreSQL + SQLAlchemy 2.0 (Async)
* **Caching/Session Store**: Redis
* **Auth**: OAuthlib (Starlette)
* **Mailing**: FastAPI-Mail (BackgroundTasks for non-blocking email delivery)

## 🏗 Database Schema

The core relational models include:
* **User**: Central profile management with verification tracking.
* **OAuthAccount/Provider**: Separate tables to support multiple social login providers per user.
* **Post & Comment**: Implements recursive relationships for nested comment threads (self-referencing `parent_id`).

## 📅 Project Roadmap

This project is in active development. The following features are planned in order of priority:
1.  **Chat Bot**: An AI bot set up to answer project related questions.
2.  **Social Graph**: Friends system and user relationships.
3.  **Real-time Communication**: Private chat between friends.
4.  And all the other ideas that I will come up with.
5.  **DevOps**: Dockerization and unit/integration testing.

## 🕷 Known Issues
1.  Currently using auto-incrementing Integers for IDs. Will transition to **UUID4** for better security.
2.  Lack of oauth account linking. The project will eventually support accounts with multiple login options.
3.  DB optimizations. There are some lazy written SQLAlchemy queries. Project too big to care about every little optimization.
4.  Some places could be more DRY.
5.  The limiter limits by ip of the household. Not an issue for developmnet.
6.  Hashing exclusive to user sessions and profile data. Will expand the cache use to other areas in the future.
7.  Can't use github with hidden email to register.
