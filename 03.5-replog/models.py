from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    member_name: str = Field(index=True)
    exercise: str = Field(index=True)
    sets: int = Field(ge=0, le=5)
    reps: int = Field(ge=0)
    weight_kg: int = Field(ge=0)
    logged_at: datetime = Field(default_factory=datetime.now)


class WorkoutCreate(SQLModel):
    member_name: str
    exercise: str
    sets: int = Field(ge=0, le=5)
    reps: int
    weight_kg: int

class WorkoutRead(SQLModel):
    id: int
    member_name: str
    exercise: str
    sets: int
    reps: int
    weight_kg: int
    logged_at: datetime

class WorkoutUpdate(SQLModel):
    exercise: Optional[str] = Field(default=None)
    sets: Optional[int] = Field(default=None, ge=0, le=5)
    reps: Optional[int] = Field(default=None, ge=0)
    weight_kg: Optional[int] = Field(default=None, ge=0)