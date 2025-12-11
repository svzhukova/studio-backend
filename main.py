from fastapi import FastAPI

from routers.users import router as users_router
from routers.abonements import router as abonements_router
from routers.schedule import router as schedule_router

app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "API работает!"}

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(abonements_router, prefix="/abonements", tags=["Abonements"])
app.include_router(schedule_router, prefix="/schedule", tags=["Schedule"])
