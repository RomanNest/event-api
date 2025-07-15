from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.routes.auth_routes import router as auth_router
from app.routes.event_routes import router as event_router
from app.routes.booking_routes import router as booking_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(event_router)
app.include_router(booking_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Event API",
        version="1.0.0",
        description="API for events and bookings with JWT authentication",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter your JWT token like this: **Bearer &lt;token&gt;**",
        }
    }

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
