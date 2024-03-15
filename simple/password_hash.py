import bcrypt
import secrets

# 平文のパスワード
password = "tim1234".encode('utf-8')

# パスワードをハッシュ化
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# ハッシュ化されたパスワードを表示
print(hashed.decode('utf-8'))

# 実行結果 : $2b$12$hIr46Ha2UGYPBGQSwHDGQewiSA8I24Z4Y1d3lnR.O1pkK2afJ4z1G


# 32バイトのランダムな文字列を生成
secret_key = secrets.token_hex(32)
print(secret_key)