from flask import Blueprint, request, jsonify, g
import json

from forms import PageInfoCreateForm, PageHeaderUpdateForm, PageContentUpdateForm, PageInfoDeleteForm
from data import response_from_message, ResponseText, NoteMessage, PageMessage

def create_page_endpoint(services):
    page_view = Blueprint('page_view', __name__)

    jwt_service = services.jwt_service
    note_service = services.note_service
    page_service = services.page_service

    # create
    @page_view.route('/create', methods=['POST'])
    @jwt_service.login_required
    @note_service.confirm_auth
    def page_create():
        """페이지 생성 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :request: 페이지 생성을 위한 페이지 정보를 포함한 json 객체:
            {
                "noteId":str    # 노트 id
            }
        :response: 상태, 결과메시지, 데이터를 포함한 json 객체:
            {
                "state": str,           # 상태
                "message": str,         # 결과 메시지
                "data": {               # 반환하는 데이터
                        "pageId": str   # 생성한 페이지 id
                }
            }
        """
        form = PageInfoCreateForm(meta={"csrf": False})
        if not form.validate():
            return json.dumps(form.errors), 400

        body = request.json
        new_page = {
            'title': body['title'],
            'keyword': body['keyword'],
            'content': body['content'],
            'note_id': body['noteId']
        }

        try:
            page_id = page_service.create_new_page(new_page)

            if isinstance(page_id, PageMessage):
                message = response_from_message(ResponseText.FAIL.value, page_id.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, PageMessage.CREATE.value, {'pageId': page_id})), 201


    # read
    @page_view.route('', methods=['GET'])
    @jwt_service.login_required
    @page_service.confirm_auth
    def page():
        """페이지 정보 조회 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :request: 노트 id를 포함한 query:
            {
                "pageId": int   # 노트 id
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,           # 상태
                "message": str,         # 결과 메시지
                "data": {               # 반환하는 데이터
                    "pageId": int,      # 페이지 id
                    "title": str,       # 페이지 제목
                    "keyword": str,     # 페이지 키워드
                    "content": str,     # 페이지 내용
                    "noteId": int,      # 노트 id
                    "createdAt": str,   # 페이지 생성일
                    "updatedAt": str    # 페이지 마지막 수정일
                }
            }
        """
        page_id = request.args.get('pageId')

        try:
            page = page_service.get_user_chosen_page(page_id)

            if isinstance(page, PageMessage):
                message = response_from_message(ResponseText.FAIL.value, page.value)
                if page == PageMessage.FAIL_NOT_EXISTS:
                    return jsonify(message), 400
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, PageMessage.READ.value, {
            "pageId": page['page_id'],
            "title": page['title'],
            "keyword": page['keyword'],
            "content": page['content'],
            "noteId": page['note_id'],
            "createdAt": page['created_at'],
            "updatedAt": page['updated_at']
        })), 200

    @page_view.route('/list', methods=['GET'])
    @jwt_service.login_required
    @note_service.confirm_auth
    def page_list():
        """페이지 리스트 조회 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :request: 노트 id를 포함한 query:
            {
                "noteId": int   # 노트 id
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,               # 상태
                "message": str,             # 결과 메시지
                "data": {                   # 반환하는 데이터
                    pageList: [{
                        "pageId": int,      # 페이지 id
                        "title": str,       # 페이지 제목
                        "keyword": str,     # 페이지 키워드
                        "content": str,     # 페이지 내용
                        "noteId": int,      # 노트 id
                        "createdAt": str,   # 페이지 생성일
                        "updatedAt": str    # 페이지 마지막 수정일
                    }]
                }
            }
        """
        note_id = request.args.get('noteId')

        try:
            page_list = page_service.get_list_of_page(note_id)

            if isinstance(page_list, PageMessage):
                message = response_from_message(ResponseText.FAIL.value, page_list.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, NoteMessage.READ.value, {
            'pageList': [{
                "pageId": page['page_id'],
                "title": page['title'],
                "keyword": page['keyword'],
                "content": page['content'],
                "noteId": page['note_id'],
                "createdAt": page['created_at'],
                "updatedAt": page['updated_at']
            } for page in page_list]
        })), 200


    # update
    @page_view.route('/update-header', methods=['POST'])
    @jwt_service.login_required
    @page_service.confirm_auth
    def page_update_header():
        """페이지 헤더 수정 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :request: 수정할 페이지 정보를 포함한 json 객체:
            {
                "pageId": int,  # 페이지 id
                "title": str,   # 페이지 제목
                "keyword": str  # 페이지 키워드
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,           # 상태
                "message": str,         # 결과 메시지
                "data": {               # 반환하는 데이터
                    "updatedAt": str    # 페이지 수정 날짜
                }
            }
        """
        # form = PageHeaderUpdateForm(meta={"csrf": False})
        # if not form.validate():
        #     return json.dumps(form.errors), 400

        body = request.json
        page_header = {
            'title': body['title'],
            'keyword': body['keyword'],
            'page_id': body['pageId']
        }

        try:
            updated_page = page_service.update_header(page_header)

            if isinstance(updated_page, PageMessage):
                message = response_from_message(ResponseText.FAIL.value, updated_page.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, PageMessage.UPDATE.value, {'updatedAt': updated_page})), 200

    @page_view.route('/update-content', methods=['POST'])
    @jwt_service.login_required
    @page_service.confirm_auth
    def page_update_content():
        """페이지 내용 수정 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :request: 수정할 페이지 정보를 포함한 json 객체:
            {
                "pageId": int,  # 페이지 id
                "content": str    # 페이지 제목
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,           # 상태
                "message": str,         # 결과 메시지
                "data": {               # 반환하는 데이터
                    "updatedAt": str    # 페이지 수정 날짜
                }
            }
        """
        # form = PageContentUpdateForm(meta={"csrf": False})
        # if not form.validate():
        #     return json.dumps(form.errors), 400

        body = request.json
        page_content = {
            'content': body['content'],
            'page_id': body['pageId']
        }

        try:
            updated_page = page_service.update_content(page_content)

            if isinstance(updated_page, PageMessage):
                message = response_from_message(ResponseText.FAIL.value, updated_page.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, PageMessage.UPDATE.value, {'updatedAt': updated_page})), 200


    # delete
    @page_view.route('/delete', methods=['POST'])
    @jwt_service.login_required
    @page_service.confirm_auth
    def page_delete():
        """노트 삭제 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :request: 삭제할 노트 id를 포함한 json 객체:
            {
                "pageId": int   # 노트 id
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,       # 상태
                "message": str,     # 결과 메시지
            }
        """
        form = PageInfoDeleteForm(meta={"csrf": False})
        if not form.validate():
            return json.dumps(form.errors), 400

        body = request.json
        page_id = body['pageId']

        try:
            deleted_page = page_service.delete_page(page_id)

            if isinstance(deleted_page, PageMessage):
                message = response_from_message(ResponseText.FAIL.value, deleted_page.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, PageMessage.DELETE.value)), 200


    return page_view
