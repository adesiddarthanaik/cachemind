from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import CacheMindException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(CacheMindException)
    async def cachemind_exception_handler(
        request: Request,
        exc: CacheMindException,
    ):

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": exc.__class__.__name__,
                    "message": str(exc),
                }
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request,
        exc: Exception,
    ):

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "type": "InternalServerError",
                    "message": str(exc),
                }
            },
        )
