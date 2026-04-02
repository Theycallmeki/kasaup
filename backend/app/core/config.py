import os


class Settings:

    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "705273b57368097b876a4a1599814a0e98059045ef88998083bf2f389943fd89")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")

        self.ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "")

        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_REGION = os.getenv("AWS_REGION")
        self.AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")

    def cors_origins(self):
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin]


settings = Settings()