from flask import Flask
from backend.db import init_db, mongo
from routes.transaction_routes import trans_bp

def create_app():
    app = Flask(__name__)
    init_db(app)
    mongo.init_app(app)

    # load transaction routes
    app.register_blueprint(trans_bp)
    return app
