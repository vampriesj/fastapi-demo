from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=20, example="john_doe")
    email: str = Field(..., example="john.doe@example.com")
    age: int = Field(..., gt=0, example=30)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    age: int

@app.post("/users/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    # Simulate user creation and return a response
    new_user = UserResponse(id=1, username=user.username, email=user.email, age=user.age)
    return new_user