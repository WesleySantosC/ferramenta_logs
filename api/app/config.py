import os


class Settings:

    # JWT

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "troque_essa_chave_em_producao"
    )

    ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 horas


settings = Settings()