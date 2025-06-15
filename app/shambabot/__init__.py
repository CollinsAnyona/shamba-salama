from flask import Blueprint

shambabot_bp = Blueprint('shambabot', __name__)

from . import routes 