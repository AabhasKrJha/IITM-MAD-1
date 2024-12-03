from flask import Flask, session, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from HSA.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class SessionUser:
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role

@app.before_request
def load_user():
    user_data = session.get('user')  
    if user_data:
        g.user = SessionUser(user_data['id'], user_data['name'], user_data['role'])
    else:
        g.user = None

@app.after_request
def add_cache_control(response):
    # Prevent caching for the login page
    if request.endpoint in ['login', 'signup'] or 'login' in request.path or 'signup' in request.path:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# registering all routes / blueprints

from HSA.blueprints.main_bp.routes import main
app.register_blueprint(main)

from HSA.blueprints.auth_bp.routes import auth
app.register_blueprint(auth)

from HSA.blueprints.admin_bp.routes import admin
app.register_blueprint(admin)

from HSA.blueprints.dashboard_bp.routes import dashboard
app.register_blueprint(dashboard)

from HSA.blueprints.booking_bp.routes import booking
app.register_blueprint(booking)

# registring API routes
from HSA.api.routes import api
app.register_blueprint(api)

# Custom CLI commands
import HSA.clis
app.cli.add_command(HSA.clis.create_admin_command)