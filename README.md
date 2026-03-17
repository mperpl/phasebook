# FastAPI Social Media API  
> **Early Development**. Core Auth, Session management, and caching functional. Social features actively evolving.

An asynchronous backend service built in **Python 3.12**. This project focuses on scalability and efficient session management using **FastAPI**, **SQLAlchemy**, and **Redis**.

---

## 🚀 Technical Highlights

### 🔐 Hybrid Session Management
Unlike standard stateless JWT implementations, this project uses a **Stateful Hybrid Approach**:
* **Client-Side**: Signed session cookies via `SessionMiddleware` for secure transport.
* **Server-Side**: Session tracking in **Redis**.
* **Benefit**: Allows for absolute control over user sessions, including **instant logout from all devices** and protection against stale session hijacking.

---

### ⚡ Performance Optimization (Caching Strategy)
* **Redis Hash Caching**: User profiles and frequently accessed metadata are stored as Redis Hashes to reduce PostgreSQL load.
* **Session Refresh Strategy**: TTL-based refresh mechanism to keep active sessions alive without excessive writes.
* **Selective Cache Usage**: Currently focused on sessions and user data, with plans to expand caching to other high-traffic areas (e.g., feeds, likes).

---

### 🔗 OAuth2 Flow
* Supports **Google, GitHub, and Facebook** social logins.

---

### 🛠 Security & Reliability
* **Rate Limiting**: Integrated `slowapi` for basic protection on sensitive endpoints.
* **Background Tasks**: Non-blocking email delivery using `FastAPI-Mail`.
* **Data Integrity**: Validation via **Pydantic v2** and modern Python typing.

---

## 🛠 Tech Stack

* **Framework**: FastAPI  
* **Database**: PostgreSQL + SQLAlchemy 2.0 (Async)  
* **Caching/Session Store**: Redis  
* **Auth**: OAuthlib (Starlette)  
* **Containers**: Docker
* **Mailing**: FastAPI-Mail  

---

## 🏗 Database Schema

The core relational models include:
* **User**: Central profile management with verification tracking.
* **OAuthAccount/Provider**: Supports multiple social login providers per user.
* **Post & Comment**: Recursive relationships for nested comment threads.

---

## 📅 Project Roadmap

This project is in active development. The following features are planned:

1.  **Chat System**: Private chats and group chats.  
2.  **Online Status**: Presence tracking for users.  
3.  **Likes System**: Optimized (avoid direct DB writes on every interaction).  
4.  **Feed System**: Core content delivery (likely complex).  
5.  **Social System**: Friends system and relationships.  
6.  **Pagination Refactor**: Move to cursor-based pagination.  
7.  **Media Support**: Additional media in posts (images, etc.).  
8.  **Payments**: Stripe integration (donations / optional features).  
9.  **AI Chatbot**: Project-related assistant.  
10. **AI Moderation**: Content filtering for text (and later media).  
11. **AI Summarization**: Discussion summaries (top-level comments focus).  
12. **Testing**: Unit and integration coverage.  
13. **Logging**: Better exception handling and logging.  
14. **General Improvements**: Fixing known issues and ongoing refactors.  

> These are unordered and subject to change.

---

## 🕷 Known Issues

1.  IDs are still auto-incrementing integers (planned migration to UUID).  
2.  OAuth account linking is incomplete.  
3.  Some SQLAlchemy queries are not optimized.  
4.  Codebase could be more DRY in certain areas.  
5.  Rate limiting is currently IP-based.  
6.  Redis usage is still limited in scope.  
7.  GitHub login does not work with hidden emails.  