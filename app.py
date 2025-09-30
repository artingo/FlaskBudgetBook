from flask import Flask, render_template
from backend.db import mongo, init_db

app = Flask(__name__)
init_db(app)
@app.route('/')
def hello_world():
    return f"DB connection: {mongo.db}"

if __name__ == '__main__':
    app.run()