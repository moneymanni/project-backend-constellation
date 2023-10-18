from flask import Blueprint, request, jsonify, g

from data import response_from_message, ResponseText, TagMessage

def create_tag_endpoint(services):
    tag_view = Blueprint('tag_view', __name__)

    jwt_service = services.jwt_service
    page_service = services.page_service
    tag_service = services.tag_service

    # create
    @tag_view.route('/create', methods=['POST'])
    @jwt_service.login_required
    def tag_create():
        return

    @tag_view.route('/link', methods=['POST'])
    @jwt_service.login_required
    def tag_link():
        return


    # read
    @tag_view.route('/list-on-page', methods=['GET'])
    @jwt_service.login_required
    def tag_list_on_page():
        return


    @tag_view.route('/list-in-note', methods=['GET'])
    @jwt_service.login_required
    def tag_list_in_note():
        return


    # update
    @tag_view.route('/update', methods=['POST'])
    @jwt_service.login_required
    def tag_update():
        return


    # delete
    @tag_view.route('/delete', methods=['POST'])
    @jwt_service.login_required
    def tag_delete():
        return


    return tag_view
