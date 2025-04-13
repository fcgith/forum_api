from fastapi import FastAPI
from routers.auth import router as auth_router
from services.utils import generate_token, decode_token

app = FastAPI()

# routers go here
app.include_router(auth_router, prefix="/auth")

# testing JWT generation
@app.get("/")
async def root():
    return generate_token({"data": "hello world"})

@app.get("/decode")
async def root(token: str):
    return decode_token(token)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)