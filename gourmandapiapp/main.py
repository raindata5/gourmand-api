import logging
from fastapi import FastAPI
from .routers import business, businessholdings, authusers, auth
from fastapi.security import OAuth2PasswordBearer
import os
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import (
    FastAPI,
    status,
    HTTPException,
    Request,
    Form,
    Depends
)

from gourmandapiapp import models, oauth2, schemas
from .db import get_db, start_redis
from sqlalchemy.orm import Session

logger = logging.getLogger()
logger.setLevel(logging.INFO)
templates = Jinja2Templates(directory="gourmandapiapp/templates")

app = FastAPI()
print('hello %s' % os.environ['NAME'])

app.include_router(business.router)
app.include_router(businessholdings.router)
app.include_router(authusers.router)
app.include_router(auth.router)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        'index.html', {"request": request.headers}
    )

@app.get("/secure_index", )
def index(request: Request,  db: Session = Depends(get_db), user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user)):
    return templates.TemplateResponse(
        'index.html', {"request": request.headers}
    )
