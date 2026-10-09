from flask import Flask
from routes.application_routes import application_bp

app = Flask(__name__)

app.register_blueprint(application_bp)