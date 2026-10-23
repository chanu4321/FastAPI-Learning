from fastapi.responses import JSONResponse
from fastapi import Request
from models import Workout


class MemberNotFoundError(Exception):
    def __init__(self, member_name: str):
        self.member_name = member_name


class WorkoutNotFoundError(Exception):
    def __init__(self, workout: Workout):
        self.workout = workout


async def member_not_found_handler(request: Request, exc: MemberNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "member not found",
            "message": f"member {exc.member_name} not found",
            "member": exc.member_name
        }
    )

async def workout_not_found_handler(request: Request, exc: WorkoutNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Workout not found",
            "message": f"No Workout with given details",
            "workout": exc.workout
        }
    )