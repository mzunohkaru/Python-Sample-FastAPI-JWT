from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "11c3551b1c715c884a73e2361e6715eef293c7e402d5e1ce9365ff9b27690531"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


db = {
    "tim": {
        "username": "tim",
        "full_name": "Tim Ruscica",
        "email": "tim@gmail.com",
        # パスワードをハッシュ化する
        "hashed_password": "$2b$12$2Ss8aodwv5mZjR1Ofee86.OgtdlekDXCtdB6xH.l/nUMd9K73tmXa",
        "disabled": False,
    }
}


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


# パスワードのハッシュ化と検証に使用されるCryptContextオブジェクトを作成
pwd_context = CryptContext(
    # ハッシュ化スキームとしてbcryptを使用
    schemes=["bcrypt"],
    # 古いハッシュを自動的に新しいハッシュに更新
    deprecated="auto",
)

# OAuth2の"password"フローを使用してトークンを取得するためのスキームを定義。
#   このスキームは、ユーザーが認証情報（ユーザー名とパスワード）を提供し、
#   その認証情報を使用してトークンを取得するために使用されます
oauth2_scheme = OAuth2PasswordBearer(
    # tokenUrl : トークンを取得するためのURLを指定
    tokenUrl="token"
)

app = FastAPI()


# 平文のパスワードとハッシュ化されたパスワードが、一致するかどうかを確認します
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# 平文のパスワードをハッシュ化します
def get_password_hash(password):
    return pwd_context.hash(password)


# ユーザー名をキーとしてデータベースからユーザー情報を取得します
def get_user(db, username: str):
    if username in db:
        # 指定されたusernameに対応するユーザー情報をuser_data(辞書型)として取得
        user_data = db[username]

        print("user_data", user_data)

        # 辞書がUserInDBのインスタンスに変換
        # 取得したユーザー情報をオブジェクトとして扱うことができ、属性(username, email, disabledなど)にアクセスすることが容易になります
        # **を辞書の前に置くことで、その辞書のキーと値をキーワード引数として関数やクラスのコンストラクタに渡すことができます
        return UserInDB(**user_data)


# ユーザー名とパスワードを使用してユーザーを認証します
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    # ユーザーが存在しない場合
    if not user:
        return False
    # パスワードが一致しない場合
    if not verify_password(password, user.hashed_password):
        return False

    print("user", user)

    # ユーザー情報を返します
    return user


# 与えられたデータからアクセストークンを生成します
# expires_delta : 有効期限の指定をします
def create_access_token(data: dict, expires_delta: timedelta or None = None):
    # 与えられたデータ（辞書型）をコピー
    to_encode = data.copy()
    # 有効期限が指定されている場合
    if expires_delta:
        # 現在の時間（UTC）にその期間を加えてトークンの有効期限を設定
        expire = datetime.now(ZoneInfo("Asia/Tokyo")) + expires_delta
    # 有効期限が指定されていない場合
    else:
        # 現在の時間（UTC）から15分後をトークンの有効期限として設定
        expire = datetime.now(ZoneInfo("Asia/Tokyo")) + timedelta(minutes=15)
    # 有効期限をexpというキーでエンコードするデータに追加
    to_encode.update({"exp": expire})

    print("to_encode", to_encode)

    # データをエンコードし、JWTを生成
    encoded_jwt = jwt.encode(
        # エンコードにはSECRET_KEYとALGORITHM（ここでは"HS256"）が使用されます
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    print("encoded_jwt", encoded_jwt)

    # 生成されたJWTを返します
    return encoded_jwt


# 与えられたトークンから現在のユーザーを取得します
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 認証が失敗した場合に発生させる例外を定義
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,  # ステータスコード401（未認証）
        detail="Could not validate credentials",  # エラーメッセージ
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print("get_current_user token", token)

        # 与えられたトークンをデコード
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        print("get_current_user payload", payload)

        # デコードされたペイロードからsub（subject）を取得。( この場合は、ユーザー名 )を取得する
        username: str = payload.get("sub")

        print("get_current_user username", username)

        # ユーザー名がNoneの場合 = 認証が失敗
        if username is None:
            raise credential_exception  # 上で定義した例外を発生
        # ユーザー名からTokenDataオブジェクトを作成
        token_data = TokenData(username=username)

        print("get_current_user token_data", token_data)

    # トークンが無効な場合
    except JWTError:
        raise credential_exception  # 上で定義した例外を発生
    # データベースからユーザー情報を取得
    user = get_user(db, username=token_data.username)
    # ユーザーがデータベースに存在しない場合 = 認証が失敗
    if user is None:
        raise credential_exception  # 上で定義した例外を発生

    print("get_current_user user", user)

    # ユーザー情報を返します
    return user


# 現在のユーザーがアクティブなユーザーであることを確認します
async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    # ユーザーが無効な場合
    if current_user.disabled:
        raise HTTPException(
            status_code=400, detail="Inactive user"
        )  # 例外を発生させます

    return current_user


# ユーザー名とパスワードを使用してログインし、アクセストークンを取得します
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# 現在のユーザーの情報を取得します
@app.get(
    "/users/me/", response_model=User
)  # response_model=User : レスポンスの形状をUserモデルに基づいて定義
async def read_users_me(
    # get_current_active_user関数から返されるユーザー情報をcurrent_userに注入
    current_user: User = Depends(get_current_active_user),
):
    return current_user


# 現在のユーザーが所有するアイテムを取得します
@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]


pwd = get_password_hash("tim1234")
print(pwd)
