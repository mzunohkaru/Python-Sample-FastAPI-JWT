from peewee import SqliteDatabase, Model, AutoField, CharField, TextField

db = SqliteDatabase("db.sqlite3")


class User(Model):
    id = AutoField(primary_key=True)
    username = CharField(100)
    password = CharField(100)
    refresh_token = TextField(null=True)

    class Meta:
        database = db

# テーブルを削除する
db.drop_tables([User])

db.create_tables([User])

# ユーザーデータ挿入
User.create(username="nao", password="nao1234")
User.create(username="たくま", password="taku1234")


