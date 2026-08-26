# app.py

import os
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from urllib.parse import quote_plus
from database.models import db, User

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tonematch2026')

    # Build database connection from individual variables
    password = quote_plus(os.getenv('MYSQL_PASSWORD', ''))
    host = os.getenv('MYSQL_HOST', 'localhost')
    port = os.getenv('MYSQL_PORT') or os.getenv('MYSQLPORT') or '3306'
    user = os.getenv('MYSQL_USER', 'root')
    database = os.getenv('MYSQL_DB', 'tonematch')

    print(f"Connecting to: {host}:{port}/{database}")

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max

    # Initialise database
    db.init_app(app)

    # Initialise login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to use ToneMatch'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth
    from routes.main import main
    app.register_blueprint(auth)
    app.register_blueprint(main)

    # Create tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)