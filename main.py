from typing import List

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST

from routers.auth import router as auth_router
from routers.user import router as user_router
from routers.conversations import router as conversation_router
from routers.topics import router as topics_router

app = FastAPI()

# routers go here
app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/users")
app.include_router(conversation_router, prefix="/conversations")
app.include_router(topics_router, prefix="/topics")


# Handle Pydantic exception validation error for frontend
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    errors: List[str] = [error["msg"].replace("Value error,", "Invalid data:") for error in exc.errors()]
    return JSONResponse\
    (
        status_code=HTTP_400_BAD_REQUEST,
        content={"detail": "<br />".join(errors)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)