from typing import Union

from data import LinkMessage

class LinkService:
    def __init__(self, link_dao):
        self.link_dao = link_dao

    # create
    def create_new_link(self, new_link: dict) -> Union[bool, LinkMessage]:
        """페이지간 연결을 새로 생성합니다.
        그리고 생성 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 LinkMessage를 반환합니다.

        :param new_link: 연결 정보를 포함한 딕셔너리:
            {
                'page_id': int,         # 페이지 id
                'linked_page_id': int   # 연결할 페이지 id
                'linkage': double       # 페이지 간 연결 강도
            }
        :return: 생성 성공 여부 (True/False)
        """
        try:
            link = self.link_dao.get_link_info(new_link)

            if link:
                return LinkMessage.FAIL_IS_EXISTS

            is_created = self.link_dao.insert_link_info(new_link)
        except Exception as e:
            return LinkMessage.ERROR

        return is_created


    # read
    def get_link_list_on_page(self, page_id: int) -> Union[list[dict], LinkMessage]:
        """페이지 id로 페이지 내 연결 정보를 조회합니다.
        만약 에러가 발생하면 LinkMessage를 반환합니다.

        :param page_id: 조회할 페이지 id
        :return: 연결 정보가 포함된 리스트:
            [{
                'page_id': int,         # 페이지 id
                'linked_page_id': int,  # 연결할 페이지 id
                'linkage': double,      # 페이지 간 연결 강도
                'created_at': str       # 생성일
            }]
        """
        try:
            link_list = self.link_dao.find_link_list_by_page_id(page_id)

            for link in link_list:
                if link['page_id'] != int(page_id):
                    if link['page_id'] != page_id:
                        link['page_id'], link['linked_page_id'] = link['linked_page_id'], link['page_id']
        except Exception as e:
            return LinkMessage.ERROR

        return link_list

    def get_link_list_in_note(self, note_id: int) -> Union[list[dict], LinkMessage]:
        """노트 id로 노트 내 연결 정보를 조회합니다.
        만약 에러가 발생하면 LinkMessage를 반환합니다.

        :param note_id: 조회할 노트 id
        :return: 연결 정보가 포함된 리스트:
            [{
                'page_id': int,         # 페이지 id
                'linked_page_id': int,  # 연결할 페이지 id
                'linkage': double,      # 페이지 간 연결 강도
                'created_at': str       # 생성일
            }]
        """
        try:
            link_list = self.link_dao.find_link_list_by_note_id(note_id)
        except Exception as e:
            return LinkMessage.ERROR

        return link_list


    # delete
    def delete_link(self, link: dict) -> Union[bool, LinkMessage]:
        """페이지 간 연결 정보로 연결 정보를 삭제합니다.
        그리고 삭제 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 LinkMessage를 반환합니다.

        :param link: 페이지간 연결 정보를 포함한 딕셔너리:
            {
                'page_id': int,         # 페이지 id
                'linked_page_id': int   # 연결된 페이지 id
            }
        :return: 삭제 성공 여부 (True/False)
        """
        try:
            is_deleted = self.link_dao.delete_link_info(link)
        except Exception as e:
            return LinkMessage.ERROR

        return is_deleted
