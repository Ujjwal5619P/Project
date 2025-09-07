from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routers import reports
from app.database import Base, engine
from app.routers import reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hazard Reports API")
app.include_router(reports.router)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Allow requests from your frontend



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

