from flask import render_template, Flask
from backend.db import init_db
from routes.category_routes import cat_bp
from routes.transaction_routes import trans_bp
from routes.user_routes import user_bp

app = Flask(__name__)
# establishes DB connection, loads roots and starts the Flask server
init_db(app)

# load routes
app.register_blueprint(cat_bp)
app.register_blueprint(user_bp)
app.register_blueprint(trans_bp)

@app.route('/')
def root():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
