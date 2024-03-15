# FastAPI Command

$ uvicorn api.main:app --reload


## Docker Command

$ docker compose up --build
$ docker compose up
$ docker-compose up -d

## 新しいPythonパッケージを追加した場合
$ docker-compose build --no-cache

## データベース (Postgres) へのアクセス
$ docker-compose exec db psql -U root -d users

## データベースのマイグレーション
$ docker-compose run app sh -c "cd api && python migrate_db.py"

## データ追加
INSERT INTO users (username, full_name, email, hashed_password, disabled) VALUES ('tim', 'Tim Ruscica', 'tim@gmail.com', '$2b$12$2Ss8aodwv5mZjR1Ofee86.OgtdlekDXCtdB6xH.l/nUMd9K73tmXa', FALSE);