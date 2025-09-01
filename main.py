from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine

app = FastAPI(title="mobile talon")

app.add_middleware(
    CORSMiddleware,
    allow_methods=["*"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_origins=["*"],
)

Base.metadata.create_all(engine)