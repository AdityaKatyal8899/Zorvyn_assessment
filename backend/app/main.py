from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, records, dashboard
from app.db.session import engine
from app.db.base import Base
Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Financial Dashboard API",
    description="Backend for a financial dashboard with RBAC, focused on Admin functionality.",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router)
app.include_router(records.router)
app.include_router(dashboard.router)


""" uvicorn app.main:app --reload"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
