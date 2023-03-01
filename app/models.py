from sqlalchemy import Table, Column, Integer, String, LargeBinary, Float, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    role = Column(String, nullable=False, default="user")
    temporary_password = Column(
        String, nullable=True, unique=True, default=None)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
