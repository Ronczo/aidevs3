import os
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from dotenv import load_dotenv

from endpoints import router

app = FastAPI()


@app.middleware("http")
async def check_token(request: Request, call_next):
    authorization_token: str = request.headers.get("Authorization")

    if authorization_token:
        if authorization_token != SECRET_TOKEN:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content="Token is not valid"
            )
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Authorization token is missing"
        )

    response = await call_next(request)
    return response

app.include_router(router)

load_dotenv()

API_KEY = os.getenv("OPEN_AI_API_KEY")
AGENT_KEY = os.getenv("AGENT_KEY")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

