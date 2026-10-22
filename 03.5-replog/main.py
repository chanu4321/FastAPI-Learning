from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Database tables created")
    yield
    print("Success")


app = FastAPI(
    title="RepLog",
    description="A Gym workout log API",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "Welcome to Replog workout API"}