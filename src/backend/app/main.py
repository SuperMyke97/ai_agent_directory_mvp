from fastapi import Depends, FastAPI
from backend.app.routers import users
from backend.app.database import init_db
from dotenv import load_dotenv
from pathlib import Path
import os

path = Path(".env")
load_dotenv(dotenv_path=path)

app = FastAPI(dependencies=[Depends(init_db)])
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Hello AI Directory Application!"}

print(os.getenv("DB_HOST"))

# {
#   "full_name": "Michael Ayodeji",
#   "username": "Supermyke",
#   "email": "supermyke@gmail.com",
#   "password": "supermyke"
# }