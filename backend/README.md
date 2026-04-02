# Role-Based Financial Dashboard Backend

## 1. Project Overview

This project is a powerful, secure backend system designed for a financial dashboard application. Built with FastAPI, the system manages financial data, facilitates comprehensive user management, and exposes dashboard analytics. A core pillar of this architecture is its strict Role-Based Access Control (RBAC), ensuring that multiple user roles—Admin, Analyst, and Viewer—can safely interact with the system under clearly defined and rigorously enforced permissions.

## 2. Tech Stack

- **FastAPI**: High-performance asynchronous web framework.
- **SQLAlchemy**: Robust ORM for database interactions.
- **PostgreSQL / SQLite**: Relational database storage (SQLite configured for local development).
- **Pydantic**: Strict data validation and schema serialization.

## 3. Architecture Overview

The application follows a clean, modular Service Layer Architecture to decouple business logic from routing, enhancing maintainability and testability.

- `models/` → SQLAlchemy database schema definitions.
- `schemas/` → Pydantic models for request/response validation.
- `routers/` → API endpoint definitions and route-level controllers.
- `services/` → Core business logic and database interactions.
- `core/` → RBAC enforcement, dependency injection, and security logic.
- `db/` → Database session management and engine configuration.

## 4. Features

### User Management (Admin Only)

- Create new users
- View the system's registered users
- Update user roles and status boundaries

### Record Management

- Create financial records (Admin only)
- Read financial records (Admin + Analyst)
- Update and delete existing financial records (Admin only)

### Dashboard Analytics

- **Summary**: High-level calculation of totals (All roles)
- **Category breakdown**: Grouped distribution of resources (Admin + Analyst)
- **Recent activity**: Chronological fetch of the latest entries (Admin + Analyst)

## 5. RBAC Design

Role-Based Access Control is the backbone of this system's security payload. Permissions are evaluated on every request through FastAPI’s native dependency injection (`Depends()`), ensuring logic exists centrally rather than being scattered across routes.

- **Admin**: Unrestricted operational capacity. Full access to create, read, update, and delete users and records, alongside full dashboard visualization.
- **Analyst**: Focused on insights. Permitted read-only access to raw financial records and complete access to all dashboard analytics.
- **Viewer**: Strictly limited boundary access. Only permitted to fetch the `/dashboard/summary` for abstract financial overviews without seeing raw database entries.

## 6. API Endpoints

### `/users`

- `GET /users` - Retrieve all users
- `POST /users` - Register a new user
- `PATCH /users/{id}` - Modify user details

### `/records`

- `GET /records` - Retrieve a paginated list of financial records
- `POST /records` - Add a new financial record
- `GET /records/{id}` - Retrieve a specific record
- `PATCH /records/{id}` - Update a specific record
- `DELETE /records/{id}` - Delete a specific record

### `/dashboard`

- `GET /dashboard/summary` - Fetch total incomes, expenses, and net balances
- `GET /dashboard/categories` - Fetch aggregated category sums
- `GET /dashboard/recent` - Fetch the latest temporal activity

## 7. QA Validation Summary

The backend infrastructure has undergone rigorous Quality Assurance testing and validation.

- **Backend Fully Tested**: All endpoints operate flawlessly according to their domain logic.
- **No Functional Defects**: Zero systemic logic errors or crashes were identified natively within the backend.
- **RBAC Validated**: Access control limits boundaries accurately for all 3 defined roles natively intercepting unauthorized writes/reads with HTTP `403 Forbidden` responses.
- **Edge Cases Handled**: Bad data boundaries are trapped cleanly avoiding core runtime application panics.

## 8. Edge Case Handling

- **Invalid IDs**: Path lookups against non-existent database identifiers gracefully return `404 Not Found`.
- **Invalid Payload**: Improper types or missing fields are trapped by Pydantic dependencies, triggering a strict `422 Unprocessable Entity` response.
- **Empty Database**: Dashboard analytical aggregations safely process sets devoid of database records without triggering null-reference crashes.
- **Type Validation**: Sub-zero financial inputs and string bounds enforce type safety directly at the serialization layer.

## 9. How to Run the Project

1. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic passlib[bcrypt]
   ```
2. **Launch the Server:**
   ```bash
   uvicorn app.main:app --reload
   ```
3. **Open API Documentation:**
   Navigate your browser to `http://127.0.0.1:8000/docs` to interface with the interactive Swagger sandbox.

### Environment configuration

Sensitive configuration values (for example database connection strings or API keys) should be supplied via environment variables or a local `.env` file during development. The application reads `SQLALCHEMY_DATABASE_URL` from the environment and falls back to a local SQLite file when not provided.

Create a `backend/.env` (excluded from git) with entries like:

```env
# backend/.env
SQLALCHEMY_DATABASE_URL=sqlite:///./test.db
```

For production, set `SQLALCHEMY_DATABASE_URL` to your production database connection string (e.g., a PostgreSQL URI).

## 10. How to Test RBAC

For the scope of this implementation, the backend identifies users via a mock authentication layer parsing the `x-mock-role` HTTP header.

You can simulate roles by injecting this header using `curl`, Postman, or ThunderClient:

```http
x-mock-role: admin
x-mock-role: analyst
x-mock-role: viewer
```

**Example via cURL:**

```bash
curl -X GET "http://127.0.0.1:8000/records/" -H "x-mock-role: analyst"
```

## 11. Design Decisions

- **Service Layer Pattern**: Business logic is separated from router controllers. This allows services to be called outside the web context (e.g., background tasks, scripts) and vastly improves the testing lifecycle.
- **Dependency-Based RBAC**: Centralizing authorization checks natively within FastAPI `Depends()` enforces security dynamically before endpoints even execute securely routing the validation phase.
- **Database Aggregation**: Mathematical aggregations for the dashboard queries happen natively inside the database via `func.sum()` optimizations guaranteeing massive scale improvements vs python-native math logic.
- **Mock Authentication**: Utilizing `x-mock-role` safely abstracts real implementation bounds preventing the bloat of OAuth wiring strictly for RBAC testing while demonstrating clear API scope limits.

## 12. Future Improvements

- **JWT Authentication**: Full-chain cryptographic bearer logic integrated securely across users securely.
- **Rate Limiting**: Protect costly dashboard aggregation queries from recursive API polling attacks.
- **Advanced Filtering**: Enable sophisticated endpoint bounds (e.g., specific date ranges or strict category isolations) across the `/records/` queries.
- **Pagination Enhancements**: Strengthen limits with token-based cursors natively replacing basic skips.
