from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    pg_oltp_api_db: str
    pg_oltp_api_port: str
    pg_oltp_api_host: str
    pg_oltp_api_password: str
    pg_oltp_api_user: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ALGORITHM: str
    SECRET_KEY: str
    pg_oltp_api_db_test: str
    pg_oltp_api_host_test: str
    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_KEY: str
    class Config:
        env_file = ".env"


settings = Settings()
config = {
    'development': settings
}