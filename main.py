from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import Base, engine


@asynccontextmanager
async def lifespan(fastapp: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    print("Server shutting down")


fastapp = FastAPI(lifespan=lifespan)

fastapp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)


@fastapp.get("/")
async def root():
    return {"message": "Welcome to the ASRS Backend Service!"}
