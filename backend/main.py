from contextlib import asynccontextmanager
from database.redis import redis_client
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from endpoints import ai, auth, users, posts
from core.limiter import limiter
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()

app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    settings.DOMAIN,
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    session_cookie="authlib_session",
    same_site="lax",
    https_only=settings.COOKIE_SECURE,
    secret_key=settings.MIDDLEWARE_SECRET_KEY
)

app.include_router(ai.router, prefix="/ai", tags=["ai"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
