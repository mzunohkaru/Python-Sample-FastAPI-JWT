from fastapi import FastAPI
from os import environ as env

from api.routers import users

app = FastAPI()
app.include_router(users.router)

@app.get("/")
def index():
    return {"Secret": f"{env['MY_VARIABLE']}"}



# from typing import List, Tuple
# from sqlalchemy.engine import Result

# import api.models.users as users_model


# from fastapi import Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from datetime import datetime, timedelta
# from zoneinfo import ZoneInfo
# from jose import JWTError, jwt
# from passlib.context import CryptContext

# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# from api.models.users import User as UserModel
# import api.schemas.users as users_schema
# from api.db import get_db

# SECRET_KEY = "11c3551b1c715c884a73e2361e6715eef293c7e402d5e1ce9365ff9b27690531"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


# # パスワードのハッシュ化と検証に使用されるCryptContextオブジェクトを作成
# pwd_context = CryptContext(
#     # ハッシュ化スキームとしてbcryptを使用
#     schemes=["bcrypt"],
#     # 古いハッシュを自動的に新しいハッシュに更新
#     deprecated="auto",
# )

# # OAuth2の"password"フローを使用してトークンを取得するためのスキームを定義。
# #   このスキームは、ユーザーが認証情報（ユーザー名とパスワード）を提供し、
# #   その認証情報を使用してトークンを取得するために使用されます
# oauth2_scheme = OAuth2PasswordBearer(
#     # tokenUrl : トークンを取得するためのURLを指定
#     tokenUrl="token"
# )

# app = FastAPI()


# # 平文のパスワードとハッシュ化されたパスワードが、一致するかどうかを確認します
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)


# # 平文のパスワードをハッシュ化します
# def get_password_hash(password):
#     return pwd_context.hash(password)


# # ユーザー名をキーとしてデータベースからユーザー情報を取得します
# async def get_user(db: AsyncSession, username: str):
#     async with db() as session:
#         result = await session.execute(
#             select(UserModel).filter(UserModel.username == username)
#         )
#         user = result.scalars().first()
#         return user


# # ユーザー名とパスワードを使用してユーザーを認証します
# async def authenticate_user(db: AsyncSession, username: str, password: str):
#     user = await get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False

#     return user


# # 与えられたデータからアクセストークンを生成します
# # expires_delta : 有効期限の指定をします
# def create_access_token(data: dict, expires_delta: timedelta or None = None):
#     # 与えられたデータ（辞書型）をコピー
#     to_encode = data.copy()
#     # 有効期限が指定されている場合
#     if expires_delta:
#         # 現在の時間（UTC）にその期間を加えてトークンの有効期限を設定
#         expire = datetime.now(ZoneInfo("Asia/Tokyo")) + expires_delta
#     # 有効期限が指定されていない場合
#     else:
#         # 現在の時間（UTC）から15分後をトークンの有効期限として設定
#         expire = datetime.now(ZoneInfo("Asia/Tokyo")) + timedelta(minutes=15)
#     # 有効期限をexpというキーでエンコードするデータに追加
#     to_encode.update({"exp": expire})

#     print("to_encode", to_encode)

#     # データをエンコードし、JWTを生成
#     encoded_jwt = jwt.encode(
#         # エンコードにはSECRET_KEYとALGORITHM（ここでは"HS256"）が使用されます
#         to_encode,
#         SECRET_KEY,
#         algorithm=ALGORITHM,
#     )

#     print("encoded_jwt", encoded_jwt)

#     # 生成されたJWTを返します
#     return encoded_jwt


# # 与えられたトークンから現在のユーザーを取得します
# async def get_current_user(
#     token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
# ):
#     credential_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credential_exception
#         # awaitを使用して非同期のget_user関数を呼び出し
#         user = await get_user(db, username=username)
#         if user is None:
#             raise credential_exception
#     except JWTError:
#         raise credential_exception
#     return user


# # 現在のユーザーがアクティブなユーザーであることを確認します
# async def get_current_active_user(
#     current_user: users_schema.UserInDB = Depends(get_current_user),
# ):
#     # ユーザーが無効な場合
#     if current_user.disabled:
#         raise HTTPException(
#             status_code=400, detail="Inactive user"
#         )  # 例外を発生させます

#     return current_user


# # ユーザー名とパスワードを使用してログインし、アクセストークンを取得します
# @app.post("/token", response_model=users_schema.Token)
# async def login_for_access_token(
#     form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
# ):
#     user = await authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# # 現在のユーザーの情報を取得します
# @app.get(
#     "/users/me/", response_model=users_schema.User
# )  # response_model=User : レスポンスの形状をUserモデルに基づいて定義
# async def read_users_me(
#     # get_current_active_user関数から返されるユーザー情報をcurrent_userに注入
#     current_user: users_schema.User = Depends(get_current_active_user),
# ):
#     return current_user


# # 現在のユーザーが所有するアイテムを取得します
# @app.get("/users/me/items")
# async def read_own_items(
#     current_user: users_schema.User = Depends(get_current_active_user),
# ):
#     return [{"item_id": 1, "owner": current_user}]


# @app.get("/test")
# async def search_user(
#     db: AsyncSession = Depends(get_db),
# ) -> List[str]:  # 戻り値の型をList[str]に変更
#     username = "tim"
#     result: Result = await db.execute(
#         select(
#             users_model.User.username,
#         ).where(users_model.User.username == username)  # "tim"と一致するユーザー名を検索
#     )
#     # 検索結果からユーザー名のリストを直接返す
#     return [user[0] for user in result.all()]


# pwd = get_password_hash("tim1234")
# print(pwd)
