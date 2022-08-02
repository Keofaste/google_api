from pydantic import BaseSettings


class Settings(BaseSettings):
    usd_code = 'R01235'


settings = Settings()
