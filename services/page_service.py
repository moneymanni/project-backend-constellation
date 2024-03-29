from flask import request, Response, g
from functools import wraps
from typing import Union
import json

from data import response_from_message, ResponseText, PageMessage

class PageService:
    def __init__(self, page_dao):
        self.page_dao = page_dao

    # verify
    # 요청한 사용자와 페이지 소유자(사용자)가 같은 사용자인지 확인하는 데코레이터
    def confirm_auth(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == 'GET':
                page_id = request.args.get('pageId')
            elif request.method == 'POST':
                body = request.json
                page_id = body['pageId']

            if page_id is not None:
                try:
                    page_owner_id = self.page_dao.find_page_owner_id_by_page_id(page_id)
                except Exception as e:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), status=500)

                if page_owner_id == -1:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_EXISTS.value)), status=400)
                elif page_owner_id != g.user_id:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_PERMISSION.value)), status=401)
            else:
                return Response(json.dumps(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_EXISTS.value)), status=400)
            return f(*args, **kwargs)
        return decorated_function

    # def is_included_same_note(self, page_id: int, page_id_to_compare: int) -> Union[bool, PageMessage]:
    #     """두 개의 페이지가 같은 노트에 포함되어 있는지 검증합니다.
    #     만약 에러가 발생하면 PageMessage를 반환합니다.
    #
    #     :param page_id: 페이지 id
    #     :param page_id_to_compare: 검증할 페이지 id
    #     :return: 같은 노트에 포함되어 있는지 (True/False)
    #     """
    #     try:
    #         note_id = self.page_dao.find_note_id_by_page_id(page_id)
    #         note_id_to_compare = self.page_dao.find_note_id_by_page_id(page_id_to_compare)
    #     except Exception as e:
    #         return PageMessage.ERROR
    #     finally:
    #         if note_id is None or note_id_to_compare is None:
    #             return PageMessage.ERROR
    #         elif note_id == -1 or note_id_to_compare == -1:
    #             return PageMessage.FAIL_NOT_EXISTS
    #
    #     return True if note_id == note_id_to_compare else False

    # 두 개의 페이지가 같은 노트에 포함되어 있는지 확인하는 데코레이터
    def is_included_same_note(self, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == 'GET':
                page_id = request.args.get('pageId')
                linked_page_id = request.args.get('linkedPageId')
            elif request.method == 'POST':
                body = request.json
                page_id = body['pageId']
                linked_page_id = body['linkedPageId']

            if page_id is not None and linked_page_id is not None:
                try:
                    note_id = self.page_dao.find_note_id_by_page_id(page_id)
                    note_id_to_compare = self.page_dao.find_note_id_by_page_id(linked_page_id)
                except Exception as e:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, PageMessage.ERROR.value)), status=500)

                if note_id == -1 or note_id_to_compare == -1:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_EXISTS.value)), status=400)
                if note_id != note_id_to_compare:
                    return Response(json.dumps(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_SAME_NOTE.value)), status=400)
            else:
                return Response(json.dumps(response_from_message(ResponseText.FAIL.value, PageMessage.FAIL_NOT_EXISTS.value)), status=400)
            return f(*args, **kwargs)
        return decorated_function


    # create
    def create_new_page(self, new_page: dict) -> Union[int, PageMessage]:
        """페이지를 새로 생성합니다.
        그리고 생성한 페이지 id를 반환합니다.
        만약 정상적으로 생성되지 않거나 에러가 발생하면 PageMessage를 반환합니다.

        :param new_page: 생성할 페이지 정보를 포함한 딕셔너리:
            {
                'note_id': int, # 노트 id
                'title': str,   # 페이지 제목
                'keyword': str, # 페이지 키워드
            }
        :return: 생성된 페이지 id
        """
        try:
            page_id = self.page_dao.insert_page_info(new_page)
        except Exception as e:
            return PageMessage.ERROR

        return page_id if page_id else PageMessage.ERROR


    # read
    def get_user_chosen_page(self, page_id: int) -> Union[dict, PageMessage]:
        """페이지 id로 페이지 정보를 조회합니다.
        만약 페이지가 존재하지 않거나 에러가 발생하면 PageMessage를 반환합니다.

        :param page_id: 조회할 페이지 id
        :return: 페이지 정보를 포함한 딕셔너리:
            {
                'page_id': int,     # 페이지 id
                'title': str,       # 페이지 제목
                'keyword': str,     # 페이지 키워드
                'content': str,     # 페이지 내용
                'note_id': int,     # 노트 id
                'created_at': str,  # 페이지 생성일
                'updated_at': str   # 페이지 마지막 수정일
            }
        """
        try:
            page = self.page_dao.get_page_info(page_id)
        except Exception as e:
            return PageMessage.ERROR

        return page if page else PageMessage.FAIL_NOT_EXISTS

    def get_list_of_page(self, note_id: int) -> Union[list[dict], PageMessage]:
        """노트 id로 노트 내 페이지 목록을 조회합니다.
        만약 에러가 발생하면 PageMessage를 반환합니다.

        :param note_id: 조회할 노트 id
        :return: 페이지 정보가 포함된 리스트:
            [{
                'page_id': int,     # 페이지 id
                'title': str,       # 페이지 제목
                'keyword': str,     # 페이지 키워드
                'content': str,     # 페이지 내용
                'note_id': int,     # 노트 id
                'created_at': str,  # 페이지 생성일
                'updated_at': str   # 페이지 마지막 수정일
            }]
        """
        try:
            page_list = self.page_dao.get_page_list(note_id)
        except Exception as e:
            return PageMessage.ERROR

        return page_list

    def find_page_id_and_keyword(self, note_id: int) -> Union[list[dict], PageMessage]:
        """노트 id로 페이지(id, 키워드) 목록을 조회합니다.
        만약 페이지 목록이 존재하지 않거나 에러가 발생하면 PageMessage를 반환합니다.

        :param note_id: 조회할 페이지 id
        :return: 페이지 id와 키워드를 포함한 리스트:
            [{
                'page_id': int, # 페이지 id
                'keyword': str  # 키워드
            }]
        """
        try:
            page_list = self.page_dao.find_page_id_and_keyword_by_note_id(note_id)
        except Exception as e:
            return PageMessage.ERROR

        return page_list


    # update
    def update_header(self, page: dict) -> Union[str, PageMessage]:
        """페이지 제목, 키워드를 받아 페이지 정보를 수정합니다.
        그리고 수정된 날짜를 반환합니다.
        만약 수정에 실패하거나 에러가 발생하면 PageMessage를 반환합니다.

        :param page: 페이지 정보가 포함된 딕셔너리:
            {
                'page_id': int, # 페이지 id
                'title': str,   # 페이지 제목
                'keyword': str  # 페이지 키워드
            }
        :return: 페이지 정보가 수정된 일자
        """
        try:
            is_updated = self.page_dao.update_page_header(page)

            if not is_updated:
                return PageMessage.ERROR

            updated_page = self.page_dao.get_page_info(page['page_id'])
        except Exception as e:
            return PageMessage.ERROR

        return updated_page['updated_at'] if updated_page else PageMessage.ERROR

    def update_content(self, page: dict) -> Union[str, PageMessage]:
        """페이지 내용을 받아 페이지 정보를 수정합니다.
        그리고 수정된 날짜를 반환합니다.
        만약 수정에 실패하거나 에러가 발생하면 PageMessage를 반환합니다.

        :param page: 페이지 정보를 포함한 딕셔너리
            {
                'page_id': int, # 페이지 id
                'content': str  # 페이지 내용
            }
        :return: 페이지 정보가 수정된 일자
        """
        try:
            is_updated = self.page_dao.update_page_content(page)

            if not is_updated:
                return PageMessage.ERROR

            updated_page = self.page_dao.get_page_info(page['page_id'])
        except Exception as e:
            return PageMessage.ERROR

        return updated_page['updated_at'] if updated_page else PageMessage.ERROR


    # delete
    def delete_page(self, page_id: int) -> Union[bool, PageMessage]:
        """페이지 id로 노트 정보를 삭제합니다.
        그리고 삭제 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 PageMessage를 반환합니다.

        :param page_id: 삭제할 페이지 id
        :return: 삭제 성공 여부 (True/False)
        """
        try:
            is_deleted = self.page_dao.delete_page_info(page_id)
        except Exception as e:
            return PageMessage.ERROR

        return is_deleted
