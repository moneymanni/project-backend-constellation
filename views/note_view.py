from flask import Blueprint, request, jsonify, g
import json

from forms import NoteInfoCreateForm, NoteInfoUpdateForm, NoteInfoDeleteForm
from data import response_from_message, ResponseText, NoteMessage

def create_note_endpoint(services):
    note_view = Blueprint('note_view', __name__)

    jwt_service = services.jwt_service
    note_service = services.note_service

    # create
    @note_view.route('/create', methods=['POST'])
    @jwt_service.login_required
    def note_create():
        """노트 생성 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :request: 노트 생성을 위한 노트 정보를 포함한 json 객체:
            {
                "title":str,            # 노트 제목
                "description": str,     # 노트 설명
                "sharedPermission": int # 노트 공유 권한
            }
        :response: 상태, 결과메시지, 데이터를 포함한 json 객체:
            {
                "state": str,           # 상태
                "message": str,         # 결과 메시지
                "data": {               # 반환하는 데이터
                        "noteId": str   # 생성한 노트 id
                }
            }
        """
        form = NoteInfoCreateForm(meta={"csrf": False})
        if not form.validate():
            return json.dumps(form.errors), 400

        body = request.json
        new_note = {
            'title': body['title'],
            'description': body['description'],
            'shared_permission': body['sharedPermission'],
            'user_id': g.user_id
        }

        try:
            new_note_id = note_service.create_new_note(new_note)

            if isinstance(new_note_id, NoteMessage):
                message = response_from_message(ResponseText.FAIL.value, new_note_id.value)
                return jsonify(message), 500
        except:
            return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, NoteMessage.CREATE.value, {'noteId': new_note_id})), 201


    # read
    @note_view.route('', methods=['GET'])
    @jwt_service.login_required
    @note_service.confirm_auth
    def note():
        """노트 정보 조회 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :request: 노트 id를 포함한 query:
            {
                "noteId": int   # 노트 id
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,                   # 상태
                "message": str,                 # 결과 메시지
                "data": {                       # 반환하는 데이터
                    "noteId": int,              # 노트 id
                    "title": str,               # 노트 제목
                    "description": str,         # 노트 설명
                    "sharedPermission": int,    # 노트 공유 권한
                    "userId": int,              # 사용자 id
                    "createdAt": str,           # 노트 생성일
                    "updatedAt": str            # 노트 마지막 수정일
                }
            }
        """
        note_id = request.args.get('noteId')

        try:
            note = note_service.get_user_chosen_note(note_id)

            if isinstance(note, NoteMessage):
                message = response_from_message(ResponseText.FAIL.value, note.value)
                if note == NoteMessage.FAIL_NOT_EXISTS:
                    return jsonify(message), 400
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, NoteMessage.READ.value, {
            'noteId': note['note_id'],
            'title': note['title'],
            'description': note['description'],
            'sharedPermission': note['shared_permission'],
            'userId': note['user_id'],
            'createdAt': note['created_at'],
            'updatedAt': note['updated_at']
        })), 200

    @note_view.route('/read', methods=['GET'])
    @note_service.confirm_note_permission
    def note_read():
        """노트 정보 조회 엔드포인트 (모든 사용자가)

        :request: 노트 id를 포함한 query:
            {
                "noteId": int   # 노트 id
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,           # 상태
                "message": str,         # 결과 메시지
                "data": {               # 반환하는 데이터
                        noteId: str     # 가입한 사용자 id
                }
            }
        """
        note_id = request.args.get('noteId')

        try:
            note = note_service.get_user_chosen_note(note_id)

            if isinstance(note, NoteMessage):
                message = response_from_message(ResponseText.FAIL.value, note.value)
                if note == NoteMessage.FAIL_NOT_EXISTS:
                    return jsonify(message), 400
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, NoteMessage.READ.value, {
            'noteId': note['note_id'],
            'title': note['title'],
            'description': note['description'],
            'sharedPermission': note['shared_permission'],
            'userId': note['user_id'],
            'createdAt': note['created_at'],
            'updatedAt': note['updated_at']
        })), 200

    @note_view.route('/list', methods=['GET'])
    @jwt_service.login_required
    def note_list():
        """노트 리스트 조회 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,                       # 상태
                "message": str,                     # 결과 메시지
                "data": {                           # 반환하는 데이터
                    noteList: [{
                        "noteId": int,              # 노트 id
                        "title": str,               # 노트 제목
                        "description": str,         # 노트 설명
                        "sharedPermission": int,    # 노트 공유 권한
                        "userId": int,              # 사용자 id
                        "createdAt": str,           # 노트 생성일
                        "updatedAt": str            # 노트 마지막 수정일
                    }]
                }
            }
        """
        try:
            note_list = note_service.get_list_of_user_note(g.user_id)

            if isinstance(note_list, NoteMessage):
                message = response_from_message(ResponseText.FAIL.value, note_list.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, NoteMessage.READ.value, {
            'noteList': [{
                'noteId': note['note_id'],
                'title': note['title'],
                'description': note['description'],
                'sharedPermission': note['shared_permission'],
                'userId': note['user_id'],
                'createdAt': note['created_at'],
                'updatedAt': note['updated_at']
            } for note in note_list]
        })), 200


    # update
    @note_view.route('/update', methods=['POST'])
    @jwt_service.login_required
    @note_service.confirm_auth
    def note_update():
        """노트 수정 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :request: 수정할 노트 정보를 포함한 json 객체:
            {
                "noteId": int,          # 노트 id
                "title": str,           # 노트 제목
                "description": str,     # 노트 설명
                "sharedPermission": str # 노트 공유 권한
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,           # 상태
                "message": str,         # 결과 메시지
                "data": {               # 반환하는 데이터
                    "updatedAt": str    # 노트 수정 날짜
                }
            }
        """
        form = NoteInfoUpdateForm(meta={"csrf": False})
        if not form.validate():
            return json.dumps(form.errors), 400

        body = request.json
        note = {
            'note_id': body['noteId'],
            'title': body['title'],
            'description': body['description'],
            'shared_permission': body['sharedPermission']
        }

        try:
            updated_note = note_service.update_note(note)

            if isinstance(updated_note, NoteMessage):
                message = response_from_message(ResponseText.FAIL.value, updated_note.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, NoteMessage.UPDATE.value, {'updatedAt': updated_note})), 200


    # delete
    @note_view.route('/delete', methods=['POST'])
    @jwt_service.login_required
    @note_service.confirm_auth
    def note_delete():
        """노트 삭제 엔드포인트

        :request: access 토큰이 포함된 헤더:
            { "accessToken": str }
        :request: 삭제할 노트 id를 포함한 json 객체:
            {
                "noteId": int   # 노트 id
            }
        :response: 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,       # 상태
                "message": str,     # 결과 메시지
            }
        """
        form = NoteInfoDeleteForm(meta={"csrf": False})
        if not form.validate():
            return json.dumps(form.errors), 400

        body = request.json
        note_id = body['noteId']

        try:
            deleted_note = note_service.delete_note(note_id)

            if isinstance(deleted_note, NoteMessage):
                message = response_from_message(ResponseText.FAIL.value, deleted_note.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, NoteMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, NoteMessage.DELETE.value)), 200


    return note_view
