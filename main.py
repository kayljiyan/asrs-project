from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import Base, engine, init_trays
from app.api.v1.router import v1_router
from app.db.session import SessionLocal


@asynccontextmanager
async def lifespan(fastapp: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        init_trays(db)
    yield
    print("Server shutting down")


fastapp = FastAPI(lifespan=lifespan)

fastapp.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)

fastapp.include_router(v1_router, prefix="/api/v1")


@fastapp.get("/")
async def root():
    return {"message": "Welcome to the ASRS Backend Service!"}
