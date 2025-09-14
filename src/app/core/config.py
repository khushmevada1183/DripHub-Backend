import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "DripHub Backend")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    DATABASE_URL: str = os.getenv("DATABASE_URL")  # Must be set in .env, no default
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
    LEGACY_JWT_SECRET: str = os.getenv("LEGACY_JWT_SECRET", "")
    # When true, skip automatic DB table creation on application startup.
    # Useful in hosted environments where the DB is managed separately
    # and may be temporarily unreachable during deploys.
    SKIP_DB_INIT: bool = os.getenv("SKIP_DB_INIT", "false").lower() in ("1", "true", "yes")
    # When true, include the DB exception message in /health/db responses
    # for debugging. Should NOT be enabled in production long-term.
    DB_HEALTH_VERBOSE: bool = os.getenv("DB_HEALTH_VERBOSE", "false").lower() in ("1", "true", "yes")
    # When true and SUPABASE_SERVICE_ROLE_KEY is provided, server will use the
    # Supabase Admin API to create users as already-confirmed. Use with caution.
    SUPABASE_AUTO_CONFIRM_SIGNUP: bool = os.getenv("SUPABASE_AUTO_CONFIRM_SIGNUP", "false").lower() in ("1", "true", "yes")

settings = Settings()
