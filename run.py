from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from app.auth.user_routes import auth_bp
from app.auth.user_controllers import token_in_blocklist_loader, blacklist

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'FSLesotho'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

# CORS(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return token_in_blocklist_loader(jwt_header, jwt_payload)

app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)