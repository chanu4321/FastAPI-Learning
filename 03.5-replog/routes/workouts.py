from fastapi import APIRouter, Depends, Query, HTTPException
from models import Workout, WorkoutCreate, WorkoutRead, WorkoutUpdate
from database import get_session
from sqlmodel import select, Session, func
from exceptions import MemberNotFoundError

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
    member_name: str | None = Query(default=None, description="Filter by member name"),
    exercise: str | None = Query(default=None, description="Filter by exercise"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=5, ge=1, le=20, description="Max Workouts per page")
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



@router.get("/average/{member}/{exercise}")
def avg_weight(
    member: str,
    exercise: str,
    session: Session = Depends(get_session)
):
    
    member_exist = session.exec(
        select(Workout).where(Workout.member_name == member)
    ).first()

    if not member_exist:
        raise MemberNotFoundError(member)

    avg_weight, total_count = session.exec(
        select(func.avg(Workout.weight_kg),func.count(Workout.id)).where(Workout.member_name == member).where(Workout.exercise == exercise)  ## select ends before where
        ).first()
    
    if total_count == 0:
        raise HTTPException(status_code=404, detail=f"No log found of {exercise} for {member}")

    return {
        "member": member,
        "exercise": exercise,
        "average_weight" : round(avg_weight,2),
        "total_count" : total_count
    }
