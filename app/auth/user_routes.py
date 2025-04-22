from flask import Blueprint
from app.auth.user_controllers import signup, signin, signout

auth_bp = Blueprint('auth_bp', __name__)

auth_bp.route('/signup', methods=['POST'])(signup)
auth_bp.route('/signin', methods=['POST'])(signin)
auth_bp.route('/signout', methods=['POST'])(signout)