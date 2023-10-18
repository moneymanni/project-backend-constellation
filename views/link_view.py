from flask import Blueprint, request, jsonify, g
import json

from forms import LinkInfoCreateForm, LinkInfoDeleteForm
from data import response_from_message, ResponseText, LinkMessage, PageMessage

def create_link_endpoint(services):
    link_view = Blueprint('link_view', __name__)

    jwt_service = services.jwt_service
    note_service = services.note_service
    page_service = services.page_service
    link_service = services.link_service

    # create
    @link_view.route('/create', methods=['POST'])
    @jwt_service.login_required
    @page_service.confirm_auth
    def link_create():
        """페이지 간 연결 생성 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :request: 페이지 id를 포함한 json 객체:
            {
                "pageId": int,          # 노트 id
                'linkedPageId': int,    # 연결될 페이지 id
                'linkage': double       # 연결 강도
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,                       # 상태
                "message": str,                     # 결과 메시지
            }
        """
        # form = LinkInfoCreateForm(meta={"csrf": False})
        # if not form.validate():
        #     return json.dumps(form.errors), 400

        body = request.json
        new_link = {
            'page_id': body['pageId'],
            'linked_page_id': body['linkedPageId'],
            'linkage': body['linkage']
        }

        try:
            is_created = link_service.create_new_link(new_link)

            if isinstance(is_created, LinkMessage):
                message = response_from_message(ResponseText.FAIL.value, is_created.value)
                if is_created == LinkMessage.FAIL_IS_EXISTS:
                    return jsonify(message), 400
                elif is_created == LinkMessage.ERROR:
                    return jsonify(message), 500
            if not is_created:
                return jsonify(response_from_message(ResponseText.FAIL.value, LinkMessage.ERROR.value)), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, LinkMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, LinkMessage.CREATE.value)), 201


    # read
    @link_view.route('/list-on-page', methods=['GET'])
    @jwt_service.login_required
    @page_service.confirm_auth
    def link_list_on_page():
        """페이지와 연결된 연결 리스트 조회 엔드포인트

        :request access token이 담긴 헤더:
            {
                "accessToken": str      # 사용자의 access 토큰
            }
        :request: 페이지 id를 포함한 query:
            {
                "pageId": int   # 페이지 id
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,                       # 상태
                "message": str,                     # 결과 메시지
                "data": {                           # 반환하는 데이터
                    linkList: [{
                        "pageId": int,          # 페이지 id
                        "linkedPageId": int,    # 연결된 페이지 id
                        "linkage": double,      # 연결 강도
                        "createdAt": str,       # 페이지 생성일
                    }]
                }
            }
        """
        page_id = request.args.get('pageId')

        try:
            link_list = link_service.get_link_list_in_note(page_id)

            if isinstance(link_list, LinkMessage):
                message = response_from_message(ResponseText.FAIL.value, link_list.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, LinkMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, LinkMessage.READ.value, {
            'linkList': [{
                'pageId': link['page_id'],
                'linkedPageId': link['linked_page_id'],
                'linkage': link['linkage'],
                'createdAt':link['created_at']
            } for link in link_list]
        }))

    @link_view.route('/list-in-note', methods=['GET'])
    @jwt_service.login_required
    @note_service.confirm_auth
    def link_list_in_note():
        """노트 내 연결 리스트 조회 엔드포인트

        :request access token이 담긴 헤더:
            {
                "accessToken": str      # 사용자의 access 토큰
            }
        :request: 노트 id를 포함한 query:
            {
                "noteId": int   # 노트 id
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,                       # 상태
                "message": str,                     # 결과 메시지
                "data": {                           # 반환하는 데이터
                    pageList: [{
                        "pageId": int,          # 페이지 id
                        "LinkedPageId": int,    # 연결된 페이지 id
                        "Linkage": double,      # 연결 강도
                        "createdAt": str,       # 페이지 생성일
                    }]
                }
            }
        """
        note_id = request.args.get('noteId')

        try:
            link_list = link_service.get_link_list_in_note(note_id)

            if isinstance(link_list, LinkMessage):
                message = response_from_message(ResponseText.FAIL.value, link_list.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, LinkMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, LinkMessage.READ.value, {
            'linkList': [{
                'pageId': link['page_id'],
                'linkedPageId': link['linked_page_id'],
                'linkage': link['linkage'],
                'createdAt':link['created_at']
            } for link in link_list]
        }))


    # delete
    @link_view.route('/delete', methods=['POST'])
    @jwt_service.login_required
    @page_service.confirm_auth
    @page_service.is_included_same_note
    def link_delete():
        """연결 정보 삭제 엔드포인트

        :request access token이 담긴 헤더:
            {
                "accessToken": str      # 사용자의 access 토큰
            }
        :request: 두 페이지 id를 포함한 query:
            {
                "pageId": int,          # 페이지 id
                "linkedPageId": int,    # 연결된 페이지 id
            }
        :response 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,               # 상태
                "message": str,             # 결과 메시지
            }
        """
        body = request.json
        link = {
            'page_id': body['pageId'],
            'linked_page_id': body['linkedPageId']
        }

        try:
            deleted_link = link_service.delete_link(link)

            if isinstance(deleted_link, LinkMessage):
                message = response_from_message(ResponseText.FAIL.value, deleted_link.value)
                return jsonify(message), 500
            if not deleted_link:
                return jsonify(response_from_message(ResponseText.FAIL.value, LinkMessage.ERROR.value)), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, LinkMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, LinkMessage.DELETE.value)), 200


    return link_view
