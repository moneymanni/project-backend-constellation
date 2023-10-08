from flask import Flask
from sqlalchemy import create_engine
from flask_cors import CORS

from views import create_endpoint

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

    ## Business Layer
    services = Services

    ## endpoint 생성
    create_endpoint(app, services)

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
