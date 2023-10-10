from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    Form,
    Response
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from gourmandapiapp import models, schemas, utils, oauth2
from ..db import get_db
from typing import (
    Union,
    Annotated
)
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBasic,
    HTTPBasicCredentials
)
from fastapi.responses import RedirectResponse
import requests

from fastapi_login import LoginManager
from gourmandapiapp.config import settings
from fastapi_login.exceptions import InvalidCredentialsException

templates = Jinja2Templates(directory="gourmandapiapp/templates")
security = HTTPBasic()

router = APIRouter(tags=['token'])

# manager = LoginManager(settings.SECRET_KEY, token_url='/token2')


# @manager.user_loader()
# def load_user(
#     email: str,
#     db: Session = Depends(get_db)
# ):
#     user_obj = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.email == email).first()
#     return user_obj

# @router.post('/token2')
# async def login(login_form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     fetched_user = load_user(login_form_data.username)
#     if not fetched_user:
#         raise InvalidCredentialsException
#     verify_pass = utils.verification(login_form_data.password, fetched_user.password)
#     if not verify_pass:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect username or password")
#     token = manager.create_access_token(data={"userid": fetched_user.userid})
#     return {"access_token": token, "token_type": "bearer"}



def exc_handler(request: Request, exc):
    print(request.url)
    print(request.url.path)
    return RedirectResponse(url=f'/login?return_url={request.url.path}', status_code=303, headers={"return_url": request.url.path})

@router.post('/token')
async def login_token(remember_me: Annotated[bool, Form()] = False, login_form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    fetched_user = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.email == login_form_data.username).first()
    if not fetched_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect username or password")
    verify_pass = utils.verification(login_form_data.password, fetched_user.password)
    if not verify_pass:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect username or password")
    token = oauth2.create_access_token(user_data= {"userid": fetched_user.userid, 'remember_me': remember_me})
    return {"access_token": token, "token_type": "bearer"}

@router.get('/login')
def simple_login(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    return_url: str = ''
):
    default_return_url = return_url if return_url.startswith('/') else '/'
    template_response = templates.TemplateResponse(
        "login.html",
        context={
            "request": request,
            "return_url": default_return_url
        }
    )
    # template_response.
    # from urllib.parse import urlencode
    # urlencode(q_params).encode('utf-8')
    return template_response
    

@router.post('/login')
def simple_login(
    request: Request,
    response: Response,
    email: Annotated[str, Form(title="Your email you signed up with")],
    password: Annotated[str, Form(title="The Password you signed up with")],
    remember_me: Annotated[bool, Form()] = False,
    return_url: str = '',
    db: Session = Depends(get_db)
):
    user_obj = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.email == email).first()
    print(return_url)
    result = oauth2.verify_email_and_pass(
        current_email=email,
        current_password=password,
        correct_user=user_obj.email,
        correct_pass=user_obj.password
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    res = requests.post(
        request.headers.get("origin", "ronald") + "/token",
        data={
            "username":email,
            "password": password,
            "remember_me": remember_me,
        }
    )
    res_json = res.json()
    redirect_res = RedirectResponse(
        url=return_url,
        status_code=303,
    )
    redirect_res.set_cookie(key="Authorization", value=res_json["token_type"].title() + ' ' + res_json["access_token"])
    return redirect_res