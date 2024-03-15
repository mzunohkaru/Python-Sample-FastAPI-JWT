from sqlalchemy import create_engine
from api.models.users import Base

# root: データベースのユーザー名 (docker-compose -> services -> db -> environment -> POSTGRES_USER)
# password: データベースのパスワード (docker-compose -> services -> db -> environment -> POSTGRES_PASSWORD)
# postgres_db: データベースサーバーのホスト名またはIPアドレス (docker-compose -> services -> db -> container_name)
# 5432: データベースサーバーがリッスンしているポート番号 (docker-compose -> services -> db -> ports)
# users: 接続するデータベースの名前 (docker-compose -> services -> db -> environment -> POSTGRES_DB)
DB_URL = "postgresql://root:password@postgres_db:5432/users"
engine = create_engine(DB_URL, echo=True)

def reset_database():
    # テーブルを削除
    Base.metadata.drop_all(bind=engine)
    # テーブルを再作成
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_database()