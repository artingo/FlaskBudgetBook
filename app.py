from flask import render_template
from . import create_app

# establishes DB connection, loads roots and starts the Flask server
app = create_app()

@app.route('/')
def root():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)