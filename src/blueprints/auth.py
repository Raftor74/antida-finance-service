from flask import (
    Blueprint,
    request,
    session,
)
from werkzeug.security import check_password_hash

from utils.database import db
from utils.response import json_response

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
def login():
    pass


@bp.route('/logout', methods=['POST'])
def logout():
    pass
