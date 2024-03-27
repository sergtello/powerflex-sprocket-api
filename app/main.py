from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from app.modules.sprocket.routes import router as sprocket_router
from app.modules.factory.routes import router as factory_router
from app.auth import service as auth
from app.config import settings

app = FastAPI(
    title="Powerflex Sprockets Demo API",
    swagger_ui_parameters={"syntaxHighlight.theme": "nord"},
    # docs_url=settings.path_prefix + "/docs",
    # openapi_url=settings.path_prefix + "/openapi.json",
    docs_url=None,
    openapi_url=None,
    redoc_url=None
)

prefix_router = APIRouter(prefix=settings.path_prefix)


@prefix_router.get("/", include_in_schema=False)
def prefix_root():
    return {
        "ok": True,
        "message": "POWERFLEX DEMO SPROCKET API",
    }


@prefix_router.get("/docs", include_in_schema=False)
def get_swagger_documentation(username: str = Depends(auth.get_docs_username)):
    return get_swagger_ui_html(openapi_url=settings.path_prefix + "/openapi.json",
                               title="docs",
                               swagger_ui_parameters={"defaultModelsExpandDepth": -1})


@prefix_router.get("/openapi.json", include_in_schema=False)
def openapi(username: str = Depends(auth.get_docs_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=origins,
    allow_headers=origins
)

app.include_router(prefix=settings.path_prefix, router=sprocket_router)
app.include_router(prefix=settings.path_prefix, router=factory_router)

app.include_router(router=prefix_router)


@app.get("/")
def root():
    return {
        "ok": True,
        "message": "POWERFLEX DEMO SPROCKET API",
    }
