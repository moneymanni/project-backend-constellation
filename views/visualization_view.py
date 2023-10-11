from flask import Blueprint, request, jsonify


def create_visualization_endpoint(services):
    visualization_view = Blueprint('visualization_view', __name__)

    link_service = services.link_service
    page_service = services.page_service
    # jwt_service = services.jwt_service

    # node
    @visualization_view.route('/node', methods=['GET'])
    def node():
        note_id = request.args.get('noteId')

        return jsonify({
            'note_id': note_id,
            'node': page_service.find_page_id_and_keyword(note_id)
        })

    # edge
    @visualization_view.route('/edge', methods=['GET'])
    def edge():
        note_id = request.args.get('noteId')

        return jsonify({
            'note_id': note_id,
            'edge': link_service.get_link_list_in_note(note_id)
        })

    return visualization_view