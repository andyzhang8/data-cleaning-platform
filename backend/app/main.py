from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from app.config import settings
from app.routers import auth, datasets, transform
from app.models.database import Base, engine
from app.tasks import celery_app

app = FastAPI(
    title="Interactive Data Cleaning Platform",
    description="A platform for data cleaning and preprocessing",
    version="1.0.0"
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])
app.include_router(transform.router, prefix="/transform", tags=["Transformations"])

# Middleware
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# JWT Settings
@AuthJWT.load_config
def get_config():
    return settings


# Handle AuthJWT exceptions globally
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

# health check
@app.get("/health/celery", tags=["Health"])
def health_check():
    """Check the health of Celery workers."""
    try:
        ping_response = celery_app.control.ping()
        if ping_response:
            return {"status": "Celery is running", "response": ping_response}
        else:
            return {"status": "Error", "details": "No response from Celery workers"}
    except Exception as e:
        return {"status": "Error", "details": str(e)}


# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Interactive Data Cleaning Platform!"}
