# app/main.py
from fastapi import FastAPI
from app.routers import users, records, dashboard
from app.db.session import engine
from app.db.base import Base

# Create tables in the database
# Note: In a production environment, use migrations (e.g., Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Dashboard API",
    description="Backend for a financial dashboard with RBAC, focused on Admin functionality.",
    version="1.0.0"
)

# Include Routers
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Financial Dashboard API",
        "docs": "/docs",
        "status": "online"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)