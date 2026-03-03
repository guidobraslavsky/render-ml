from flask import Flask
from routes.complaints_routes import complaint_bp
from database import init_db

app = Flask(__name__)

init_db()
app.register_blueprint(complaint_bp)

if __name__ == "__main__":
    app.run(debug=True)
