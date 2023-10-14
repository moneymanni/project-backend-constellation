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
    note_dao = NoteDao(database)
    page_dao = PageDao(database)
    link_dao = LinkDao(database)
    # tag_dao = TagDao(database)

    ## Business Layer
    services = Services
    services.jwt_service = JWTService(user_dao, app.config)
    services.auth_service = AuthService(user_dao)
    services.user_service = UserService(user_dao)
    services.note_service = NoteService(note_dao)
    services.page_service = PageService(page_dao)
    services.link_service = LinkService(link_dao)
    # services.tag_service = TagService(tag_dao, page_dao)
    services.recommend_service = RecommendService()

    ## endpoint 생성
    create_endpoint(app, services)
    app.register_blueprint(create_auth_endpoint(services, app.config), url_prefix='/auth')
    app.register_blueprint(create_user_endpoint(services, app.config), url_prefix='/user')
    app.register_blueprint(create_note_endpoint(services), url_prefix='/note')
    app.register_blueprint(create_page_endpoint(services), url_prefix='/page')
    app.register_blueprint(create_link_endpoint(services), url_prefix='/link')
    # app.register_blueprint(create_tag_endpoint(services), url_prefix='/tag')
    app.register_blueprint(create_visualization_endpoint(services), url_prefix='/visualization')
    app.register_blueprint(create_recommend_endpoint(services), url_prefix='/recommend')



    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
