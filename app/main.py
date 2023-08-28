from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routers import sprocket, factory
from app import database, schemas, utils, auth
from app.config import settings

app = FastAPI(
    title="Powerflex Sprockets Demo API",
    swagger_ui_parameters={"syntaxHighlight.theme": "nord"},
    docs_url=settings.path_prefix + "/docs",
    openapi_url=settings.path_prefix + "/openapi.json",
    redoc_url=None
)

prefix_router = APIRouter(prefix=settings.path_prefix)


@prefix_router.get("/")
async def prefix_root():
    return {
        "ok": True,
        "message": "POWERFLEX DEMO SPROCKET API",
    }

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins
)

app.include_router(prefix=settings.path_prefix, router=sprocket.router)
app.include_router(prefix=settings.path_prefix, router=factory.router)

if settings.path_prefix:
    app.include_router(router=prefix_router)


@app.get("/")
async def root():
    return {
        "ok": True,
        "message": "POWERFLEX DEMO SPROCKET API",
    }
