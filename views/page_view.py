from flask import Blueprint, request, jsonify, g

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
            'title': '',
            'keyword': '',
            'content': '',
            'note_id': body['noteId']
        }

        try:
            user_is_note_owner = note_service.confirm_auth(g.user_id, new_page['note_id'])
        except Exception as e:
            user_is_note_owner = NoteMessage.ERROR
        finally:
            if user_is_note_owner == NoteMessage.ERROR:
                return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.ERROR.value)), 500
            elif not user_is_note_owner and user_is_note_owner is not None:
                return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.FAIL_NOT_PERMISSION.value)), 401
            elif user_is_note_owner == NoteMessage.FAIL_NOT_EXISTS:
                return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.FAIL_NOT_EXISTS.value)), 400

        try:
            page_id = page_service.create_new_page(new_page)
        except Exception as e:
            page_id = PageMessage.ERROR
        finally:
            if page_id is None or page_id == PageMessage.ERROR:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, PageMessage.CREATE.value, {'pageId': page_id})), 201


    # read
    @page_view.route('/list', methods=['GET'])
    @jwt_service.login_required
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
                "state": str,                       # 상태
                "message": str,                     # 결과 메시지
                "data": {                           # 반환하는 데이터
                    pageList: [{
                        "pageId": int,     # 페이지 id
                        "title": str,       # 페이지 제목
                        "keyword": str,     # 페이지 키워드
                        "content": str,     # 페이지 내용
                        "noteId": int,     # 노트 id
                        "createdAt": str,  # 페이지 생성일
                        "updatedAt": str   # 페이지 마지막 수정일
                    }]
                }
            }
        """
        note_id = request.args.get('noteId')

        try:
            user_is_note_owner = note_service.confirm_auth(g.user_id, note_id)
        except Exception as e:
            user_is_note_owner = NoteMessage.ERROR
        finally:
            if user_is_note_owner == NoteMessage.ERROR:
                return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.ERROR.value)), 500
            elif not user_is_note_owner and user_is_note_owner is not None:
                return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.FAIL_NOT_PERMISSION.value)), 401
            elif user_is_note_owner == NoteMessage.FAIL_NOT_EXISTS:
                return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.FAIL_NOT_EXISTS.value)), 400

        try:
            page_list = page_service.get_list_of_page(note_id)
        except Exception as e:
            page_list = PageMessage.ERROR
        finally:
            if page_list == PageMessage.ERROR:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500
            elif page_list == PageMessage.FAIL_NOT_EXISTS:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_EXISTS.value)), 400

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

    # @page_view.route('/shared-list', methods=['GET'])
    # def page_shared_list():
    #     return



    # update
    @page_view.route('/update-header', methods=['POST'])
    @jwt_service.login_required
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
        form = PageHeaderUpdateForm(meta={"csrf": False})
        if not form.validate():
            return json.dumps(form.errors), 400

        body = request.json
        page_header = {
            'title': body['title'],
            'keyword': body['keyword'],
            'page_id': body['pageId']
        }

        try:
            user_is_page_owner = page_service.confirm_auth(g.user_id, page_header['page_id'])
        except Exception as e:
            user_is_page_owner = PageMessage.ERROR
        finally:
            if user_is_page_owner == PageMessage.ERROR:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500
            elif not user_is_page_owner and user_is_page_owner is not None:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_PERMISSION.value)), 401
            elif user_is_page_owner == PageMessage.FAIL_NOT_EXISTS:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_EXISTS.value)), 400

        try:
            updated_page = page_service.update_header(page_header)
        except Exception as e:
            updated_page = PageMessage.ERROR
        finally:
            if updated_page == PageMessage.ERROR:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, PageMessage.UPDATE.value, {'updatedAt': updated_page})), 200

    @page_view.route('/update-content', methods=['POST'])
    @jwt_service.login_required
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
        form = PageContentUpdateForm(meta={"csrf": False})
        if not form.validate():
            return json.dumps(form.errors), 400

        body = request.json
        page_content = {
            'content': body['content'],
            'page_id': body['pageId']
        }

        try:
            user_is_page_owner = page_service.confirm_auth(g.user_id, page_content['page_id'])
        except Exception as e:
            user_is_page_owner = PageMessage.ERROR
        finally:
            if user_is_page_owner == PageMessage.ERROR:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500
            elif not user_is_page_owner and user_is_page_owner is not None:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_PERMISSION.value)), 401
            elif user_is_page_owner == PageMessage.FAIL_NOT_EXISTS:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_EXISTS.value)), 400

        try:
            updated_page = page_service.update_content(page_content)
        except Exception as e:
            updated_page = PageMessage.ERROR
        finally:
            if updated_page == PageMessage.ERROR:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, PageMessage.UPDATE.value, {'updatedAt': updated_page})), 200


    # delete
    @page_view.route('/delete', methods=['POST'])
    @jwt_service.login_required
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
            user_is_page_owner = page_service.confirm_auth(g.user_id, page_id)
        except Exception as e:
            user_is_page_owner = PageMessage.ERROR
        finally:
            if user_is_page_owner == PageMessage.ERROR:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500
            elif not user_is_page_owner and user_is_page_owner is not None:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_PERMISSION.value)), 401
            elif user_is_page_owner == PageMessage.FAIL_NOT_EXISTS:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_EXISTS.value)), 400

        try:
            deleted_page = page_service.delete_page(page_id)
        except Exception as e:
            deleted_page = PageMessage.ERROR
        finally:
            if not deleted_page or deleted_page == PageMessage.ERROR:
                return jsonify(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, PageMessage.DELETE.value)), 200


    return page_view
