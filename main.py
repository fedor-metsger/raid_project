
from flask import Flask
from src.views import main_blueprint
from src.raid_db import get_dsn, create_db as create_db, fill_db as fill_db

app = Flask(__name__)
app.register_blueprint(main_blueprint)

def main():

    DSN = get_dsn()
    if not DSN:
        print("""
    Необходимо задать параметры подключения к БД через переменные среды:
        PSTGRS_DB     - Имя базы данных
        PSTGRS_USER   - Имя пользователя
        PSTGRS_PASSWD - Пароль пользователя
        PSTGRS_HOSTNAME - Имя или адрес хоста
    """)
        return

    create_db()
    fill_db()

    app.run(port=80)

if __name__ == "__main__":
    main()