from fastapi import FastAPI

from app.api import booking_router, cancel_router, checkout_router
from app.config import get_settings

app = FastAPI(title=get_settings().app_name, version='0.1.0')

app.include_router(booking_router)
app.include_router(checkout_router)
app.include_router(cancel_router)


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok', 'environment': get_settings().app_env}


@app.get('/')
def root() -> dict[str, str]:
    return {'message': 'Booking backend is ready'}
