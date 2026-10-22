from fastapi import APIRouter, Depends, Query, HTTPException
from models import Workout, WorkoutCreate, WorkoutRead, WorkoutUpdate
from database import get_session, Session
from sqlmodel import select

router = APIRouter(prefix="/workouts", tags=["Workout Log"])

@router.post("/",response_model=WorkoutRead)
def create_workout(
    workout: WorkoutCreate,
    session: Session = Depends(get_session)
):
    db_workout = Workout(**workout.model_dump())
    session.add(db_workout)
    session.commit()
    session.refresh(db_workout)
    return db_workout



@router.get("/", response_model=list[WorkoutRead])
def list_workout(
    session: Session = Depends(get_session),
    member_name: str = Query(default=None, description="Filter by member name"),
    exercise: str = Query(default=None, description="Filter by exercise"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=5, gt=1, le=20, description="Max Workouts per page")
):

    query = select(Workout)

    if member_name:
        query = query.where(Workout.member_name == member_name)
    if exercise:
        query = query.where(Workout.exercise == exercise)

    query = query.offset(skip).limit(limit)

    workouts = session.exec(query).all()
    return workouts



@router.get("/{workout_id}", response_model=WorkoutRead)
def get_workout(
    workout_id: int,
    session: Session = Depends(get_session)
):
    workout = session.get(Workout, workout_id)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout details not found")

    return workout