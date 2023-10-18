from typing import Union

from data import TagMessage

class TagService:
    def __init__(self, tag_dao, page_dao):
        self.tag_dao = tag_dao
        self.page_dao = page_dao

    # create
    def create_new_tag(self, new_tag: dict) -> Union[int, TagMessage]:
        """태그 정보를 받아 새로운 태그를 생성하고 연결합니다.
        그리고 태그 id를 반환합니다.
        만약 이미 태그가 존재하거나 에러가 발생하면 'TagMessage'를 반환합니다.

        :param new_tag: 태그 정보가 포함된 딕셔너리:
            {
                'name': str,    # 태그명
                'page_id': int, # 페이지 id
                'note_id': int  # 노트 id
            }
        :return: 생성된 태그 id
        """
        # 태그가 이미 존재하는지 확인하고, 만약 존재하면 에러 반환
        try:
            check_tag_exists = self.tag_dao.find_tag_id_by_tag_name_and_note_id(new_tag)

            if check_tag_exists != -1:
                return TagMessage.FAIL_IS_EXISTS

            new_tag_id = self.tag_dao.insert_tag_info(new_tag)

            if new_tag_id == -1:
                return TagMessage.ERROR
            new_tag['tag_id'] = new_tag_id

            connect = self.tag_dao.insert_page_tag_list_info(new_tag)

            if not connect:
                return TagMessage.ERROR
        except Exception as e:
            return TagMessage.ERROR

        # 태그가 존재하지 않으면 생성
        # 그리고 페이지와 연결
        return new_tag_id

    def connect_tag_to_page(self, info: dict) -> Union[bool, TagMessage]:
        """태그 id와 페이지 id를 받아 연결(생성)합니다.
        만약 이미 페이지-태그 정보가 존재하거나 에러가 발생하면 'TagMessage'를 반환합니다.

        :param info: 페이지 id와 태그 id를 포함한 딕셔너리:
            {
                'page_id': int, # 페이지 id
                'tag_id': int   # 태그 id
            }
        :return: 연결(생성) 성공 여부 (True/False)
        """
        try:
            check_tag_exists = self.tag_dao.find_tag_id_by_tag_name_and_note_id(new_tag)

            if check_tag_exists == -1:
                return TagMessage.FAIL_NOT_EXISTS

            connect = self.tag_dao.insert_page_tag_list_info(info)
        except Exception as e:
            return TagMessage.ERROR

        return connect


    # reda
    def get_tag(self, tag_id: int) -> Union[dict, TagMessage]:
        """태그 id로 태그 정보를 조회합니다.
        만약 태그 정보가 존재하지 않거나 에러가 발생하면 'TagMessage'를 반환합니다.

        :param tag_id: 태그 id
        :return: 태그 정보를 포함한 딕셔너리:
            {
                'tag_id': int,  # 태그 id
                'name': str,    # 태그명
                'note_id': int  # 노트 id
            }
        """
        try:
            tag = self.tag_dao.get_tag_info(tag_id)
        except Exception as e:
            return TagMessage.ERROR

        return tag if tag else TagMessage.FAIL_NOT_EXISTS

    def get_tag_list_on_page(self, page_id: int) -> Union[list[dict], TagMessage]:
        """페이지 id로 페이지 내 태그 리스트를 조회합니다.
        만약 태그 정보가 없으면 빈 리스트를 반환하고,
        에러가 발생하면 'TagMessge'를 반환합니다.

        :param page_id: 조회할 페이지 id
        :return: 모든 태그 정보를 포함한 리스트:
            [{
                'tag_id': int,  # 태그 id
                'name': str,    # 태그 명
                'note_id': str  # 노트 id
            }]
        """
        try:
            tag_list = self.tag_dao.find_tag_list_by_page_id(page_id)
        except Exception as e:
            return TagMessage.ERROR

        return tag_list

    def get_tag_list_in_note(self, note_id: int) -> Union[list[dict], TagMessage]:
        """노트 id로 노트 내 태그 리스트를 조회합니다.
        만약 태그 정보가 없으면 빈 리스트를 반환하고,
        에러가 발생하면 'TagMessge'를 반환합니다.

        :param note_id: 조회할 노트 id
        :return: 모든 태그 정보를 포함한 리스트:
            [{
                'tag_id': int,  # 태그 id
                'name': str,    # 태그 명
                'note_id': str  # 노트 id
            }]
        """
        try:
            tag_list = self.tag_dao.find_tag_list_by_note_id(note_id)
        except Exception as e:
            return TagMessage.ERROR

        return tag_list


    # update
    def update_tag(self, tag: dict) -> Union[bool, TagMessage]:
        """태그 명을 받아 태그 정보를 수정합니다.
        그리고 수정 성공 여부(True/False)를 반환합니다.
        만약 수정에 실패하거나 에러가 발생하면 PageMessage를 반환합니다.

        :param tag: 태그 정보를 포함한 딕셔너리:
            {
                'tag_id': int,  # 태그 id
                'name': str     # 태그명
            }
        :return: 수정 성공 여부 (True/False)
        """
        try:
            is_updated = self.tag_dao.update_tag_info(tag)
        except Exception as e:
            return TagMessage.ERROR

        return is_updated


    # delete
    def delete_tag(self, tag_id: int) -> Union[bool, TagMessage]:
        """태그 id로 태그 정보를 삭제합니다.
        그리고 삭제 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 PageMessage를 반환합니다.

        :param tag_id: 태그 id
        :return: 삭제 성공 여부 (True/False)
        """
        try:
            is_deleted = self.tag_dao.delete_tag_info(tag_id)
        except Exception as e:
            return TagMessage.ERROR

        return is_deleted

    def disconnect_tag_from_page(self, info: dict) -> Union[bool, TagMessage]:
        """태그 id와 페이지 id를 받아 연결을 끊습니다(삭제).
        그리고 삭제 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 'TagMessage'를 반환합니다.

        :param info: 페이지 id와 태그 id를 포함한 딕셔너리:
            {
                'page_id': int, # 페이지 id
                'tag_id': int   # 태그 id
            }
        :return: 삭제 성공 여부 (True/False)
        """
        try:
            is_deleted = self.tag_dao.delete_page_tag_list_info(info)
        except Exception as e:
            return TagMessage.ERROR

        return is_deleted
