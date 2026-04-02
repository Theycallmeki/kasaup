import os


class Settings:

    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")

        self.ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "")

        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_REGION = os.getenv("AWS_REGION")
        self.AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")

    def cors_origins(self):
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin]


settings = Settings()