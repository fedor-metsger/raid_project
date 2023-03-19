
import json
from flask import Blueprint
from src.raid_db import RaidSession, get_dsn as get_dsn

main_blueprint = Blueprint('main_blueprint', __name__)

raid_session = None

@main_blueprint.route('/')
def page_index():
    return "Все работает"

@main_blueprint.route('/frameworks')
def page_frameworks():
    global raid_session
    if not raid_session:
        dsn = get_dsn()
        if not dsn: return """
    Необходимо задать параметры подключения к БД через переменные среды:
        PSTGRS_DB     - Имя базы данных
        PSTGRS_USER   - Имя пользователя
        PSTGRS_PASSWD - Пароль пользователя
        PSTGRS_HOSTNAME - Имя или адрес хоста
"""
    raid_session = RaidSession(dsn)
    fwks = raid_session.get_frameworks()
    if fwks:
        return json.dumps(fwks)
    else:
        return "Невозможно запросить БД"
