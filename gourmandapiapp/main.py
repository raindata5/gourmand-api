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
    Depends,
    Cookie
)

from gourmandapiapp import models, oauth2, schemas
from .db import get_db, start_redis
from sqlalchemy.orm import Session
from typing import Annotated, Any
from fastapi.staticfiles import StaticFiles
from functools import wraps, partial
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
logger = logging.getLogger()
logger.setLevel(logging.INFO)
templates = Jinja2Templates(directory="gourmandapiapp/templates")


app = FastAPI()
app.add_middleware(HTTPSRedirectMiddleware)
app.mount("/static", StaticFiles(directory="gourmandapiapp/templates/static"), name="static")
print('hello %s' % os.environ['NAME'])

app.include_router(business.router)
app.include_router(businessholdings.router)
app.include_router(authusers.router)
app.include_router(auth.router)
app.add_exception_handler(status.HTTP_401_UNAUTHORIZED, auth.exc_handler)

@app.middleware('https')
async def if_user_check_verification(
    request: Request,
    call_next,
    # Authorization: Annotated[str, Cookie()] = 'Bearer default' ,
    # db: Session = Depends(get_db)
):
    Authorization = request.cookies.get('Authorization', 'Bearer default')
    token = Authorization.split(' ')[1]
    print(request.url.path)
    if Authorization != 'Bearer default' and not request.url.path.startswith('/auth') and not request.url.path == '/':
        if userid := oauth2.verify_token(token, credentials_exception=None, strict=False).userid:
            db = next(get_db())
            user_obj = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.userid == userid).first()
            if not user_obj.verified:
                credentials_exception = HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User is yet to be verified",
                )
                resp_redirect = RedirectResponse(
                    url='/auth/unverified',
                    status_code=303
                )
                resp_redirect.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
                return resp_redirect
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

@app.get("/")
def index(request: Request, user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user_lax)):
    return templates.TemplateResponse(
        'index.html', {"request": request.headers, "user_obj": user_obj}
    )


# test endpoint for getting a token from a cookie
@app.get("/index_secure", )
def index(request: Request,  db: Session = Depends(get_db), user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user_strict)):
    # print(request.headers)
    return templates.TemplateResponse(
        'index.html', {"request": request.headers, "user_obj": user_obj}
    )


class PermissionRequired:
    def __init__(self, permission):
        self.permission = permission

    def __call__(self, function) -> Any:
        @wraps(function)
        def wrapped_function(*args, **kwargs)-> Any:
            user_obj: models.AuthUserModelORM = kwargs.get('user_obj')
            if not user_obj.can(self.permission):
                credentials_exception = HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"User doesn't have {self.permission} permission",
                )
                logging.info(f"User doesn't have {self.permission} permission")
                raise credentials_exception
            return function(*args, **kwargs)
        
        return wrapped_function
    
def permission_required(
    request: Request,
    permission: int,
    user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user_strict),
):
    if not user_obj.can(permission):
        credentials_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User doesn't have {permission} permission",
        )
        logging.info(f"User doesn't have {permission} permission")
        raise credentials_exception
    return permission

admin_required = partial(
    permission_required,
    permission=schemas.Permission.ADMIN
)

@app.get('/for_admins')
# @PermissionRequired(schemas.Permission.ADMIN)
def for_admins(
    request: Request,  
    db: Session = Depends(get_db), 
    user_obj: models.AuthUserModelORM = Depends(oauth2.get_current_user_strict),
    result: int = Depends(admin_required),
):
    return templates.TemplateResponse(
        'index.html', {"request": request.headers, "user_obj": user_obj}
    )
