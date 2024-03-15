from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Postgresのdockerコンテナに対して接続するセッションを作成
# root : docker-compose -> services -> db -> environment -> POSTGRES_USER
# password : docker-compose -> services -> db -> environment -> POSTGRES_PASSWORD
# users : docker-compose -> services -> db -> environment -> POSTGRES_DB
# host : docker-compose -> services -> db -> container_name
ASYNC_DB_URL = "postgresql+asyncpg://root:password@postgres_db:5432/users"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()

# DBへのアクセス
async def get_db():
    async with async_session() as session:
        yield session