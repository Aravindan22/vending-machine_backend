from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_NAME="vending-machine"
DB_USER="2owmshm2357i6m46q2ol"
DB_PASSWORD="pscale_pw_tvZWeTZ60i482f7SZdEkTKmL0L5qx3AA1UCjJRxnjNi"
DB_HOST="us-east.connect.psdb.cloud"
DB_PORT=3306
MYSQL_ATTR_SSL_CA="/etc/ssl/certs/ca-certificates.crt"


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()