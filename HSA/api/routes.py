from flask import Blueprint

api = Blueprint("api", __name__, url_prefix="/api")

from .users.routes import users_api
api.register_blueprint(users_api)

from .services.routes import services_api
api.register_blueprint(services_api)

from .bookings.routes import bookings_api
api.register_blueprint(bookings_api)