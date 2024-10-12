from fastapi import FastAPI
from .routers import items, clock_in

app = FastAPI(
    title="TrackIT API",
    description="FastAPI application that performs CRUD operations on Items and Clock-in",
    version="1.0.0"
)

app.include_router(items.router)
app.include_router(clock_in.router)

@app.get("/")
async def root():
    return {"success": True}
