from fastapi import FastAPI

app = FastAPI()

# routers go here
#
# app.include_router(....)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)