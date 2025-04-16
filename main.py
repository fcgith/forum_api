from fastapi import FastAPI
from routers.auth import router as auth_router

app = FastAPI()

# routers go here
app.include_router(auth_router, prefix="/auth")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)