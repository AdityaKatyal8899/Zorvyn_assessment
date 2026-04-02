# Role-Based Financial Dashboard Backend

A robust and modular **FastAPI** backend system designed for financial data management and analytical insights, featuring a strict **Role-Based Access Control (RBAC)** architecture.

## 🚀 Project Overview

This backend serves as the core engine for a financial dashboard, enabling users to:
- **Manage Users**: Admin-only control over user registration, roles, and status.
- **Track Finances**: Full CRUD operations for income and expense records.
- **Analyze Data**: High-level summaries and category-wise breakdowns powered by database-side aggregation.

The system is built on a **Service Layer Architecture**, ensuring that business logic is decoupled from API routing for maximum maintainability and testability.

## 🛠️ Tech Stack

- **Core Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous Python)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database**: PostgreSQL-compatible (configured for SQLite in development)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Security**: [Passlib](https://passlib.readthedocs.io/) (Bcrypt hashing)

## 📁 Project Structure

```text
app/
├── models/     # SQLAlchemy database models
├── schemas/    # Pydantic data validation & response models
├── routers/    # API endpoint definitions (Route Level RBAC)
├── services/   # Business logic (Service Layer)
├── core/       # Security, hashing, and RBAC dependencies
├── db/         # Database session & base configuration
└── main.py     # Application entrypoint & router registration
```

## 🔌 API Overview

### User APIs (Admin Only)
- `POST /users`: Register new users.
- `GET /users`: List all registered users.
- `PATCH /users/{id}`: Update user role or status.

### Record APIs
- `POST /records`: Create new financial records (Admin only).
- `GET /records`: List all records (Currently Admin only).
- `GET /records/{id}`: Retrieve specific record details.
- `PATCH /records/{id}`: Update existing records.
- `DELETE /records/{id}`: Remove record entries.

### Dashboard APIs
- `GET /dashboard/summary`: High-level overview (Income, Expense, Balance). **[All Roles]**
- `GET /dashboard/categories`: Category-wise breakdown. **[Admin, Analyst]**
- `GET /dashboard/recent`: Activity log of the latest 5 records. **[Admin, Analyst]**

## 🔐 RBAC Design

The system implements a granular access model enforced via FastAPI dependency injection:

| Role      | Access Level | Permitted Operations |
|-----------|--------------|----------------------|
| **Viewer**  | Low          | Summary analytics only. |
| **Analyst** | Medium       | Full analytics + Read-only access to records (TBD). |
| **Admin**   | High         | Full system control (User mgmt, CRUD, Analytics). |

## 📊 Current Status

- ✅ **Admin**: Fully implemented with complete system control.
- 🏗️ **Viewer**: Mostly complete (restricted to summary dashboard).
- 🕒 **Analyst**: Partially complete (access to analytics, but record access is pending).

---

## 🚧 REMAINING WORK (Next Steps)

### 1. Analyst Record Access
Extend the `GET /records` and `GET /records/{id}` endpoints to allow `Analyst` access. 
- **Goal**: Admin maintains full CRUD; Analyst gains Read-Only visibility.
- **Action**: Update `require_role([UserRole.admin, UserRole.analyst])` in the records router.

### 2. Optional Filtering (Recommended)
Enhance the record listing API to support dynamic filtering for better data exploration:
```http
GET /records?type=expense&category=food&date_from=2024-01-01
```

### 3. Pagination Improvements
Shift from basic `skip`/`limit` to validated pagination objects:
- Set maximum `limit` caps to prevent database strain.
- Standardize paginated response objects.

### 4. JWT Authentication
Transition from the current "mock user" setup to a production-ready **OAuth2 + JWT** system:
- Implement `/login` for token generation.
- Securely decode tokens in `get_current_user` dependency.

### 5. Advanced Validation
Strengthen the application with custom error handlers:
- Handle database integrity errors (unique constraint violations).
- Refine edge case handling for numeric data (negative amounts, etc.).

---

## 🏁 How to Run

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt]
   ```
2. **Launch the Server**:
   ```bash
   python app/main.py
   # OR
   uvicorn app.main:app --reload
   ```
3. **Explore Documentation**:
   Navigate to `http://localhost:8000/docs` to access the interactive Swagger UI.

## 🧠 Design Decisions

- **Service Layer**: Decoupling business logic from endpoints ensures that the API can be easily reused or extended without duplicating code.
- **Dependency-Based RBAC**: Centralizing role checks in dependencies keeps routers clean and makes auditing access levels trivial.
- **Database-Side Aggregation**: All financial calculations are performed in SQL (via `func.sum`), ensuring optimal performance even with millions of records.

## 🔜 Future Improvements

- **Trends & Forecasting**: Add analytical endpoints for monthly/yearly financial projections.
- **Ownership Filtering**: Implement logic where non-admin users only see records they created.
- **Rate Limiting**: Protect the API from abuse during analytics-heavy operations.
