import uvicorn
from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()

class UpdateUserPermission(BaseModel):
    category_id: int
    user_id: int
    permission: int = 1

@app.post("/test")
async def test_endpoint(
    data: UpdateUserPermission,
    token: str = Query(...)
):
    return data, token

uvicorn.run(app, host="127.0.0.1", port=8008)
