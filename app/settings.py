from pydantic import BaseSettings


class Settings(BaseSettings):
    usd_code: str = 'R01235'

    google_sheet_key: str

    postgres_user: str
    postgres_password: str
    postgres_db: str

    @property
    def database_url(self) -> str:
        return f'postgresql+psycopg2://' \
               f'{self.postgres_user}:{self.postgres_password}' \
               f'@postgres:5432/{self.postgres_db}'


settings = Settings()
