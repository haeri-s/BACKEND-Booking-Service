
from fastapi import Depends, FastAPI, Request, status
from server.database import database, get_db
from server.auth.routes import router as authRouter
from server.accounts.routes import router as accountRouter
from server.subscriptions.routes import router as subscriptionRouter
from server.services.routes import router as serviceRouter
from starlette.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

origins = [
    'localhost:8000',
    'localhost:5555',
    'localhost:7777',
    '127.0.0.1:8000',
    '127.0.0.1:5555',
    '127.0.0.1:7777',
]

origins = [
    '*'
]

app = FastAPI(
  title="예약 서비스",
  dependencies=[Depends(get_db)]
)
# @app.exception_handler(Exception)
# async def http_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=500,
#         content=jsonable_encoder({"detail": exc.__dict__}),
#     )
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

api_version = 'v1'
api_prefix = f'/api/{api_version}'
app.include_router(authRouter, prefix=api_prefix)
app.include_router(accountRouter, prefix=api_prefix)
app.include_router(subscriptionRouter, prefix=api_prefix)
app.include_router(serviceRouter, prefix=api_prefix)
