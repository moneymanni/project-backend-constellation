from flask import Blueprint, request, jsonify

from data import response_from_message, ResponseText, VisualizationMessage, PageMessage, LinkMessage

def create_visualization_endpoint(services):
    visualization_view = Blueprint('visualization_view', __name__)

    link_service = services.link_service
    page_service = services.page_service
    note_service = services.note_service
    jwt_service = services.jwt_service

    # node
    @jwt_service.login_required
    @note_service.confirm_auth
    @visualization_view.route('/node', methods=['GET'])
    def node():
        note_id = request.args.get('noteId')

        try:
            node_list = page_service.find_page_id_and_keyword(note_id)

            if isinstance(node_list, PageMessage):
                message = response_from_message(ResponseText.FAIL.value, node_list.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, VisualizationMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, VisualizationMessage.READ.value, {
            [{
                'pageId': node['page_id'],
                'keyword': node['keyword']
            } for node in node_list]
        })), 200

    # edge
    @jwt_service.login_required
    @note_service.confirm_auth
    @visualization_view.route('/edge', methods=['GET'])
    def edge():
        note_id = request.args.get('noteId')

        try:
            edge_list = link_service.get_link_list_in_note(note_id)

            if isinstance(edge_list, LinkMessage):
                message = response_from_message(ResponseText.FAIL.value, edge_list.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, VisualizationMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, VisualizationMessage.READ.value, {
            [{
                'pageId': edge['page_id'],
                'linkedPageId': edge['linked_page_id'],
                'linkage': edge['linkage'],
                'createdAt': edge['created_at']
            } for edge in edge_list]
        })), 200


    return visualization_view