from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from api.db import Base


class User(Base):
    # テーブル名
    __tablename__ = "users"

    # カラム
    id = Column(Integer, primary_key=True)
    username = Column(String(1024))
    email = Column(String(1024))
    full_name = Column(String(1024))
    hashed_password = Column(String(1024))
    disabled = Column(Boolean, default=False)

