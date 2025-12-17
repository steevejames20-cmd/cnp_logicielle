from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "Budgetis"
    debug: bool = True
    database_url: str = Field(default="sqlite:///./budgetis.db")
    secret_key: str = Field(default="change-me-secret")
    access_token_expire_minutes: int = 60 * 24
    free_budget_limit: int = 3
    free_saving_goal_limit: int = 1

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "Budgetis"
    debug: bool = True
    database_url: str = Field(default="sqlite:///./budgetis.db")
    secret_key: str = Field(default="change-me-secret")
    access_token_expire_minutes: int = 60 * 24
    free_budget_limit: int = 3
    free_saving_goal_limit: int = 1

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


