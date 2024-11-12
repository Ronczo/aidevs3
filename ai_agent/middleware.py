from ai_agent.main import app, SECRET_TOKEN
from fastapi import Request, HTTPException, status


@app.middleware("http")
async def check_token(request: Request, call_next):
    authorization_token: str = request.headers.get("Authorization")

    if authorization_token:
        if authorization_token != SECRET_TOKEN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token is not valid"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization token is missing"
        )

    response = await call_next(request)
    return response