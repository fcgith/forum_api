from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.user import router as user_router

app = FastAPI()

# routers go here
app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/users")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)