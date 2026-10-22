from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class Workout(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    member_name: str = Field(index=True)
    exercise: str = Field(index=True)
    sets: int = Field(ge=0, le=5)
    reps: int = Field(ge=0)
    weight_kg: float = Field(ge=0)
    logged_at: datetime = Field(default_factory=lambda:datetime.now(timezone.utc))  ## use this now


class WorkoutCreate(SQLModel):
    member_name: str
    exercise: str
    sets: int = Field(default=0, ge=0, le=5)
    reps: int = Field(ge=0)
    weight_kg: Optional[float] = Field(default=0,ge=0)

class WorkoutRead(SQLModel):
    id: int
    member_name: str
    exercise: str
    sets: int
    reps: int
    weight_kg: float
    logged_at: datetime

class WorkoutUpdate(SQLModel):
    exercise: Optional[str] = Field(default=None)
    sets: Optional[int] = Field(default=None, ge=0, le=5)
    reps: Optional[int] = Field(default=None, ge=0)
    weight_kg: Optional[float] = Field(default=None, ge=0)