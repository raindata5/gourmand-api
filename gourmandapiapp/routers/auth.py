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
    Optional,
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

templates = Jinja2Templates(directory="gourmandapiapp/templates")
security = HTTPBasic()

router = APIRouter(tags=['token'])

manager = LoginManager(settings.SECRET_KEY, token_url='/token')

@router.post('/token')
async def login(login_form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    fetched_user = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.email == login_form_data.username).first()
    if not fetched_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect username or password")
    verify_pass = utils.verification(login_form_data.password, fetched_user.password)
    if not verify_pass:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect username or password")
    token = oauth2.create_access_token(user_data= {"userid": fetched_user.userid})
    return {"access_token": token, "token_type": "bearer"}

# def load_user():
#     user_obj = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.email == email).first()

@router.get('/login')
def simple_login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        context={
            "request": request
        }
    )

@router.post('/login')
def simple_login(
    request: Request,
    response: Response,
    email: Annotated[str, Form(title="Your email you signed up with")],
    password: Annotated[str, Form(title="The Password you signed up with")],
    db: Session = Depends(get_db)
):
    user_obj = db.query(models.AuthUserModelORM).filter(models.AuthUserModelORM.email == email).first()


    result = oauth2.verify_email_and_pass(
        current_email=email,
        current_password=password,
        correct_user=user_obj.email,
        correct_pass=user_obj.password
    )
    if not result:
        # return RedirectResponse(
        #     url="/login",
        #     status_code=404
        # )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    # print(request.get("referer", ""))
    res = requests.post(
        request.headers.get("origin", "ronald") + "/token",
        data={
            "username":email,
            "password": password
        }
    )
    res_json = res.json()
    # response.set_cookie(key="Authorization", value=res_json["token_type"].title() + ' ' + res_json["access_token"])
    # print(vars(request))
    # print(res.json())
    redirect_res = RedirectResponse(
        url="/",
        status_code=303,
    )
    redirect_res.set_cookie(key="Authorization", value=res_json["token_type"].title() + ' ' + res_json["access_token"])
    return redirect_res