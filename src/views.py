
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

    fwks = raid_session.get_frameworks()
    if fwks:
        return json.dumps(fwks)
    else:
        return "Невозможно запросить БД"

@main_blueprint.route('/frameworks/<string:lang>')
def page_frameworks_by_lang(lang):
    global raid_session

    fwks = raid_session.get_frameworks_by_lang(lang)
    if fwks:
        return json.dumps(fwks)
    else:
        return "Невозможно запросить БД"