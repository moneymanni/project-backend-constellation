from flask import Flask
from sqlalchemy import create_engine
from flask_cors import CORS

from models import *
from services import *
from views import *

class Services:
    pass

def create_app(test_config = None):
    app = Flask(__name__)

    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding="utf-8", max_overflow=0)

    ## Presistence Layer
    user_dao = UserDao(database)

    ## Business Layer
    services = Services
    services.jwt_service = JWTService(user_dao, app.config)
    services.user_service = UserService(user_dao)

    ## endpoint 생성
    create_endpoint(app, services)
    app.register_blueprint(create_user_endpoint(services, app.config), url_prefix='/user')


    return app

app = create_app()

if __name__ == '__main__':
    app.run()
