
import os
from flask import Flask
import src.views as views
from src.raid_db import RaidSession, get_dsn as get_dsn

app = Flask(__name__)
app.register_blueprint(views.main_blueprint)

def main():
#     dsn = get_dsn()
#     if not dsn:
#         print("""
#     Необходимо задать параметры подключения к БД через переменные среды:
#         PSTGRS_DB     - Имя базы данных
#         PSTGRS_USER   - Имя пользователя
#         PSTGRS_PASSWD - Пароль пользователя
#         PSTGRS_HOSTNAME - Имя или адрес хоста
# """)
#         return
#     rs = RaidSession(dsn)
#
#     if rs.create_db():
#         rs.fill_db()

    views.raid_session = None

    port_num = 10000
    if {"PORT"} <= os.environ.keys():
        port_num = int(os.environ["PORT"])
        if port_num >= 1024:
            print(f"Requested to use port {port_num} by PORT environment variable")
        else:
            print(f"Setting port number {port_num} by default")
    app.run(port=port_num)

if __name__ == "__main__":
    main()