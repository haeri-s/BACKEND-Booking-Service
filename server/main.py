
from fastapi import Depends, FastAPI, Request, status
from server.database import database, get_db
from server.auth.routes import router as authRouter
from server.managers.routes import router as managerRouter
from server.subscriptions.routes import router as subscriptionRouter
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

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

@app.on_event('startup')
async def startup():
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

app.include_router(authRouter)
app.include_router(managerRouter)
app.include_router(subscriptionRouter)
