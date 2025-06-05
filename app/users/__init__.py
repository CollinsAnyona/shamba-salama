from flask import Blueprint

users_bp = Blueprint('users', __name__)
auth_bp = Blueprint('auth', __name__)

from . import routes 
from . import auth_routes
from . import expert_routes