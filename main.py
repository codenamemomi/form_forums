from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes.contact import contact_router  # Import the contact router
from api.v1.routes.early_access import early_access_router # Import the early access router

app = FastAPI()

# Allow frontend to send requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://s33jay.vercel.app",  # Your actual frontend domain
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
    
# Include the contact form routes
app.include_router(contact_router, prefix="/api/v1")
app.include_router(early_access_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}
