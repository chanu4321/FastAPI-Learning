from fastapi.responses import JSONResponse
from fastapi import Request

class MemberNotFoundError(Exception):
    def __init__(self, member_name: str):
        self.member_name = member_name


async def member_not_found_handler(request: Request, exc: MemberNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "member not found",
            "message": f"member {exc.member_name} not found",
            "member": exc.member_name
        }
        )