from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from schemas import Token as schemas_Token, User as schemas_User
from models import User as model_User

from auth import (
    get_current_user,
    get_current_user_with_refresh_token,
    create_tokens,
    authenticate,
)

app = FastAPI()


@app.post("/token", response_model=schemas_Token)
# OAuth2PasswordRequestForm型のformパラメータを受け取る
# リクエストが来たときにOAuth2PasswordRequestFormのインスタンスが自動的に作成され、関数に渡されます
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """トークン発行"""
    user = authenticate(form.username, form.password)
    return create_tokens(user.id)


@app.get("/refresh_token/", response_model=schemas_Token)
async def refresh_token(
    current_user: schemas_User = Depends(get_current_user_with_refresh_token),
):
    """リフレッシュトークンでトークンを再取得"""
    return create_tokens(current_user.id)


@app.get("/users/me/", response_model=schemas_User)
async def read_users_me(current_user: schemas_User = Depends(get_current_user)):
    """ログイン中のユーザーを取得"""
    return current_user


@app.post("/create/user")
async def create_user(username: str, password: str):
    return model_User.create(username=username, password=password)
