from sqlalchemy import text
from typing import Optional

class LinkDao:
    def __init__(self, database):
        self.db = database

    # create
    def insert_link_info(self, link: dict) -> bool:
        """연결 관련 정보를 받아 페이지간 연결을 합니다.
        그리고 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 'RuntimeError' 예외가 발생합니다.

        :param link: 연결 관련 정보를 포함한 딕셔너리:
            {
                'page_id': int,         # 페이지 id
                'linked_page_id': int   # 연결할 페이지 id
                'linkage': double        # 페이지 간 연결 강도
            }
        :return: 생성 성공 여부 (True/False)
        """
        try:
            created_rowcnt = self.db.execute(text("""
                INSERT INTO link_list (
                    page_id,
                    linked_page_id,
                    linkage
                ) VALUES (
                    :page_id,
                    :linked_page_id,
                    :linkage
                )
            """), {
                'page_id': link['page_id'],
                'linked_page_id': link['linked_page_id'],
                'linkage': link['linkage']
            }).rowcount
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return created_rowcnt and created_rowcnt > 0


    # read
    def get_link_info(self, page: dict) -> Optional[dict]:
        """두 개의 페이지 id로 연결 정보를 찾습니다.
        만약 정보가 존재하지 않으면 None을 반환하고,
        에러가 발생하면 'RuntimeError' 예외가 발생합니다.

        :param page: 페이지 id가 포함되어 있는 딕셔너리:
            {
                'page_id': int,         # 페이지 id
                'linked_page_id': int   # 연결된 페이지 id
            }
        :return: 연결된 페이지 id를 포함한 딕셔너리:
            {
                'page_id': int,         # 페이지 id
                'linked_page_id': int   # 연결된 페이지 id
            } 또는 페이지 간의 연결이 없다면 None
        """
        try:
            link = self.db.execute(text("""
                SELECT
                    page_id,
                    linked_page_id
                FROM link_list
                WHERE (page_id = :page_id AND linked_page_id = :linked_page_id)
                OR (page_id = :linked_page_id AND linked_page_id = :page_id)
            """), {
                'page_id': page['page_id'],
                'linked_page_id': page['linked_page_id']
            }).fetchone()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return {
            'page_id': link['page_id'],
            'linked_page_id': link['linked_page_id']
        } if link else None

    def find_link_list_by_page_id(self, page_id: int) -> list:
        """페이지 id로 연결 정보를 조회합니다.
        그리고 페이지 id와 연결된 연결 리스트가 반환됩니다.
        만약 연결 정보가 없으면 빈 리스트를 반환하고,
        에러가 발생하면 'RuntimeError' 예외가 발생합니다.

        :param page_id: 조회할 페이지 id
        :return: 모든 연결 정보가 포함된 리스트:
            [{
                'page_id': int          # 페이지 id
                'linked_page_id': int   # 연결할 페이지 id
                'linkage': double       # 페이지 간 연결 강도
                'created_at': int       # 생성일
            }]
        """
        try:
            link_list = self.db.execute(text("""
                SELECT
                    page_id,
                    linked_page_id,
                    linkage,
                    created_at
                FROM link_list
                WHERE page_id = :page_id
                OR linked_page_id = :page_id
            """), {
                'page_id': page_id,
            }).fetchall()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return [{
            'page_id': link['page_id'],
            'linked_page_id': link['linked_page_id'],
            'linkage': link['linkage'],
            'created_at': link['created_at']
        } for link in link_list]

    def find_link_list_by_note_id(self, note_id: int) -> list:
        """노트 id로 연결 정보를 조회합니다.
        그리고 해당 노트 내의 연결 리스트가 반환됩니다.
        만약 연결 정보가 없으면 빈 리스트를 반환하고,
        에러가 발생하면 'RuntimeError' 예외가 발생합니다.

        :param note_id: 조회할 노트 id
        :return: 모든 연결 정보가 포함된 리스트:
            [{
                'page_id': int          # 페이지 id
                'linked_page_id': int   # 연결할 페이지 id
                'linkage': double       # 페이지 간 연결 강도
                'created_at': int       # 생성일
            }]
        """
        try:
            link_list = self.db.execute(text("""
                SELECT
                    link_list.page_id,
                    link_list.linked_page_id,
                    link_list.linkage,
                    link_list.created_at 
                FROM pages
                JOIN link_list ON pages.id = link_list.page_id
                WHERE pages.note_id = :note_id
            """), {
                'note_id': note_id
            }).fetchall()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return [{
            'page_id': link['page_id'],
            'linked_page_id': link['linked_page_id'],
            'linkage': link['linkage'],
            'created_at': link['created_at']
        } for link in link_list]


    # delete
    def delete_link_info(self, link: dict) -> bool:
        """연결 정보를 삭제합니다. 그리고 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 'RuntimeError' 예외가 발생합니다.

        :param link: 삭제할 연결 정보
            {
                'page_id': int,         # 페이지 id
                'linked_page_id': int   # 연결된 페이지 id
            }
        :return: 삭제 성공 여부 (True/False)
        """
        try:
            deleted_rowcnt = self.db.execute(text("""
                DELETE FROM link_list
                WHERE page_id = :page_id AND linked_page_id = :linked_page_id
                OR page_id = :linked_page_id AND linked_page_id = :page_id
            """), {
                'page_id': link['page_id'],
                'linked_page_id': link['linked_page_id']
            }).rowcount
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return deleted_rowcnt and deleted_rowcnt > 0
