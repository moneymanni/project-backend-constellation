from flask import request, Response, g
from functools import wraps
import json
from typing import Union

from data import response_from_message, ResponseText, NoteMessage

class NoteService:
    def __init__(self, note_dao):
        self.note_dao = note_dao

    # verify
    # 요청한 사용자와 노트 소유주(사용자)와 같은 사용자인지 확인하는 데코레이터
    def confirm_auth(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == 'GET':
                note_id = request.args.get('noteId')
            elif request.method == 'POST':
                body = request.json
                note_id = body['noteId']

            if note_id is not None:
                try:
                    note_owner_id = self.note_dao.find_user_id_by_note_id(note_id)
                except Exception as e:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, NoteMessage.ERROR.value)), status=500)

                if note_owner_id == -1:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, NoteMessage.FAIL_NOT_EXISTS.value)), status=400)
                elif note_owner_id != g.user_id:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, NoteMessage.FAIL_NOT_PERMISSION.value)), status=401)
            else:
                return Response(json.dumps(response_from_message(ResponseText.FAIL.value, NoteMessage.FAIL_NOT_EXISTS.value)),status=400)
            return f(*args, **kwargs)
        return decorated_function

    # 노트의 공유 권한을 확인하는 데코레이터
    def confirm_note_permission(self, f):
        def decorated_function(*args, **kwargs):
            if request.method == 'GET':
                note_id = request.args.get('noteId')
            elif request.method == 'POST':
                body = request.json
                note_id = body['noteId']

            if note_id is not None:
                try:
                    note_permission = self.note_dao.find_shared_permission_by_note_id(note_id)
                except Exception as e:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, NoteMessage.ERROR.value)), status=500)

                if note_permission == -1:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, NoteMessage.FAIL_NOT_EXISTS.value)), status=400)
                elif note_permission == 1:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, NoteMessage.FAIL_NOT_PERMISSION.value)), status=401)

                g.shared_permission = note_permission
            else:
                return Response(
                    json.dumps(response_from_message(ResponseText.FAIL.value, NoteMessage.FAIL_NOT_EXISTS.value)), status=400)

            return f(*args, **kwargs)
        return decorated_function


    # create
    def create_new_note(self, new_note: dict) -> Union[int, NoteMessage]:
        """노트의 정보를 받아 노트를 생성합니다.
        그리고 생성한 노트의 id를 반환합니다.
        만약 정상적으로 생성되지 않거나 에러가 발생하면 NoteMessage를 반환합니다.

        :param new_note: 노트의 정보가 포함된 딕셔너리:
            {
                'user_id': int,             # 사용자 id
                'title': str,               # 노트 제목
                'description': str,         # 노트 설명
                'shared_permission': int    # 노트 공유 권한
            }
        :return: 생성한 노트 id
        """
        try:
            note_id = self.note_dao.insert_note_info(new_note)
        except Exception as e:
            return NoteMessage.ERROR

        return note_id if note_id else NoteMessage.ERROR


    # read
    def get_user_chosen_note(self, note_id: int) -> Union[dict, NoteMessage]:
        """노트 id로 노트 정보를 조회합니다.
        만약 노트가 존재하지 않거나 에러가 발생하면 NoteMessage를 반환합니다.

        :param note_id: 조회할 노트 id
        :return: 노트 정보를 포함한 딕셔너리:
            {
                'note_id': int,             # 노트 id
                'title': str,               # 노트 제목
                'description': str,         # 노트 설명
                'shared_permission': int,   # 노트 공유 권한
                'user_id': int,             # 노트 소유주(사용자) id
                'created_at': str,          # 노트 생성일
                'updated_at': str           # 노트 마지막 수정일
            }
        """
        try:
            note = self.note_dao.get_note_info(note_id)
        except Exception as e:
            return NoteMessage.ERROR

        return note if note else NoteMessage.FAIL_NOT_EXISTS

    def get_list_of_user_note(self, user_id: int) -> Union[list, NoteMessage]:
        """사용자 id로 사용자의 노트 목록을 조회합니다.
        만약 에러가 발생하면 NoteMessage를 반환합니다.

        :param user_id: 조회할 사용자 id
        :return: 노트 정보를 포함한 리스트:
            [{
                'note_id': int,             # 노트 id
                'title': str,               # 노트 제목
                'description': str,         # 노트 설명
                'shared_permission': int,   # 노트 공유 권한
                'user_id': int,             # 노트 소유주(사용자) id
                'created_at': str,          # 노트 생성일
                'updated_at': str           # 노트 마지막 수정일
            }]
        """
        try:
            note_list = self.note_dao.get_note_list(user_id)
        except Exception as e:
            return NoteMessage.ERROR

        return note_list


    # update
    def update_note(self, note: dict) -> Union[str, NoteMessage]:
        """노트의 제목, 설명, 공유 권한 받아 노트 정보를 수정합니다.
        그리고 수정된 날짜를 반환합니다.
        만약 수정에 실패하거나 에러가 발생하면 NoteMessage를 반환합니다.

        :param note: 수정할 노트 정보가 포함된 딕셔너리
            {
                'note_id': int,             # 노트 id
                'title': str,               # 노트 제목
                'description': str,         # 노트 설명
                'shared_permission': int,   # 노트 공유 권한
            }
        :return: 노트 정보가 수정된 일자
        """
        try:
            is_updated = self.note_dao.update_note_info(note)

            if not is_updated:
                return NoteMessage.ERROR

            updated_note = self.note_dao.get_note_info(note['note_id'])
        except Exception as e:
            return NoteMessage.ERROR

        return updated_note['updated_at'] if updated_note else NoteMessage.ERROR


    # delete
    def delete_note(self, note_id: int) -> Union[bool, NoteMessage]:
        """노트 id로 노트 정보를 삭제합니다.
        그리고 삭제 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 NoteMessage를 반환합니다.

        :param note_id: 삭제할 노트 id
        :return: 삭제 성공 여부 (True/False)
        """
        try:
            is_deleted = self.note_dao.delete_note_info(note_id)
        except Exception as e:
            return NoteMessage.ERROR

        return is_deleted
