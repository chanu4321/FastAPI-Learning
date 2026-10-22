from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables
from routes.workouts import router as workout_router
from exceptions import member_not_found_handler, MemberNotFoundError

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Database tables created")
    yield
    print("Shutting Down")


app = FastAPI(
    title="RepLog",
    description="A Gym workout log API",
    lifespan=lifespan
)

app.include_router(workout_router)
app.add_exception_handler(MemberNotFoundError, member_not_found_handler)

@app.get("/")
def root():
    return {"message": "Welcome to Replog workout API"}