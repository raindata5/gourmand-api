from fastapi import FastAPI
from .routers import business, businessholdings, authusers, auth
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()



app.include_router(business.router)
app.include_router(businessholdings.router)
app.include_router(authusers.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"detail": "Feel free to check of the documentations at...",
            "option 1": "https://www.raindata.xyz/docs",
            "option 2": "https://www.raindata.xyz/redocs"}