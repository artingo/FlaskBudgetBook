from flask import Flask
from backend.db import init_db, mongo
from routes.category_routes import cat_bp
from routes.transaction_routes import trans_bp
from routes.user_routes import user_bp

def create_app():
    app = Flask(__name__)
    init_db(app)
    mongo.init_app(app)

    # load routes
    app.register_blueprint(cat_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(trans_bp)
    return app
