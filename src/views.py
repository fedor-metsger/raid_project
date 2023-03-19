
from flask import Blueprint

main_blueprint = Blueprint('main_blueprint', __name__)

@main_blueprint.route('/')
def page_index():
    return "Все работает"

@main_blueprint.route('/frameworks')
def page_frameworks():
    return "Frameworks"
