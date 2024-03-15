from typing import Optional

from pydantic import BaseModel


# JWT（JSON Web Token）の構造を定義します
class Token(BaseModel):
    access_token: str
    token_type: str


# トークンのペイロード部分を定義します
# ペイロード : トークンの主要な情報部分で、例えばユーザーIDや有効期限などが含まれます
class TokenData(BaseModel):
    username: str or None = None


# ユーザーの基本情報を定義します
class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None


# データベースに保存されるユーザー情報を定義します
class UserInDB(User):  # Userクラスを継承
    hashed_password: str
