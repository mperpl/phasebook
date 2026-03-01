# High-Performance FastAPI Social Media API
> **Early Development**. Core Auth & Session management functional. Social features in progress.

An asynchronous backend service built in **Python 3.12**. This project focuses on scalability and efficient session management using **FastAPI**, **SQLAlchemy**, and **Redis**.

## 🚀 Technical Highlights

* **Asynchronous Architecture**: Fully non-blocking I/O using `asyncpg` for PostgreSQL and `redis-py` for caching.
* **Multi-Layer Session Management**: 
    * Uses signed session cookies via `SessionMiddleware`.
    * Implements backend session tracking in Redis to allow for instant session invalidation and "logout from all devices" functionality.
* **OAuth2 Integration**: Supports social login via Google, GitHub, and Facebook.
    * Features a smart account-linking system that prevents duplicate accounts while maintaining security.
* **Performance Caching**: 
    * User profiles are cached in Redis Hashes to minimize expensive db hits and json string deserialization.
    * Automated cache invalidation on profile updates (Bio/Username).
* **Security & Rate Limiting**: 
    * Implements `slowapi` for fixed-window rate limiting on sensitive routes like `/login` and `/register`.
    * Password hashing using industry-standard `pwdlib`.
    * Uses Pydantic `SecretStr` for sensitive data to prevent accidental logging.

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
1.  **Content System**: Full CRUD for Posts and Comments.
2.  **Chat Bot**: An AI bot set up to answer project related questions.
3.  **Social Graph**: Friends system and user relationships.
4.  **Real-time Communication**: Private chat between friends.
5.  **ANd all the other ideas that I will come up with.
6.  **DevOps**: Dockerization and unit/integration testing.

## 🕷 Known Issues
1.  Deserve to be called a Social Media API.
2.  Currently using auto-incrementing Integers for IDs. Will transition to **UUID4** for better security.
3.  Lack of oauth account linking. The project will eventually support accounts with multiple login options.
4.  DB optimizations. There are some lazy written SQLAlchemy queries. Project too big to care about every little optimization.
5.  Some places could be more DRY.
6.  The limiter limits by ip of the household. Not an issue for developmnet.

