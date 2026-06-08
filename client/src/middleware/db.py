from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
def create_database():

    engine = create_engine(
        "mysql+pymysql://root:@localhost"
    )

    with engine.connect() as conn:
        conn.execute(
            text("CREATE DATABASE IF NOT EXISTS tayar")
        )
        conn.commit()
# Create a global SQLAlchemy object (similar to your singleton idea)
db = SQLAlchemy()