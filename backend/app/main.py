from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
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

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui():

    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dark Swagger UI</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
        <style>
            body {
                background-color: #121212;
                color: #e0e0e0;
            }
            .swagger-ui {
                filter: invert(1) hue-rotate(180deg);
            }
            .swagger-ui img {
                filter: invert(1) hue-rotate(180deg);
            }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
        <script>
            SwaggerUIBundle({
                url: "/openapi.json",
                dom_id: '#swagger-ui'
            });
        </script>
    </body>
    </html>
    """)

""" uvicorn app.main:app --reload"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
