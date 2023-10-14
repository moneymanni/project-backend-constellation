from sqlalchemy import text
from typing import Optional

class PageDao:
    def __init__(self, database):
        self.db = database

    # create
    def insert_page_info(self, page: dict) -> int:
        """ 페이지의 정보를 받아 페이지를 생성합니다.
        그리고 페이지 id를 반환합니다.
        만약 노트 정보 생성에 실패하면 -1을 반환하고,
        에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param page: 생성할 페이지 정보를 포함한 딕셔너리:
            {
                'title': str,   # 페이지 제목
                'keyword': str, # 페이지 키워드
                'content': str, # 페이지 내용
                'note_id': int  # 노트 id
            }
        :return: 생성된 페이지 id
        """
        try:
            note_id = self.db.execute(text("""
                INSERT INTO pages (
                    title,
                    keyword,
                    content,
                    note_id
                ) VALUES (
                    :title,
                    :keyword,
                    :content,
                    :note_id
                )
            """), {
                'title': page['title'],
                'keyword': page['keyword'],
                'content': page['content'],
                'note_id': page['note_id']
            }).lastrowid
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return note_id if note_id else -1


    # read
    def get_page_info(self, page_id: int) -> Optional[dict]:
        """페이지 id로 페이지 정보를 조회합니다.
        만약 페이지 정보가 존재하지 않으면 None을 반환하고,
        에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param page_id: 조회할 페이지 id
        :return: 페이지 정보가 포함된 딕셔너리:
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
            page = self.db.execute(text("""
                SELECT
                    id,
                    title,
                    keyword,
                    content,
                    note_id,
                    created_at,
                    updated_at
                FROM pages
                WHERE id = :page_id
            """), {
                'page_id': page_id
            }).fetchone()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return {
            'page_id': page['id'],
            'title': page['title'],
            'keyword': page['keyword'],
            'content': page['content'],
            'note_id': page['note_id'],
            'created_at': page['created_at'],
            'updated_at': page['updated_at']
        } if page else None

    def get_page_list(self, note_id: int) -> list:
        """노트 id로 노트의 모든 페이지 정보를 조회합니다.
        만약 페이지 정보가 존재하지 않으면 빈 리스트를 반환하고,
        에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param note_id: 조회할 노트 id
        :return: 모든 페이지 정보가 포함된 리스트:
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
            page_list = self.db.execute(text("""
                SELECT
                    id,
                    title,
                    keyword,
                    content,
                    note_id,
                    created_at,
                    updated_at
                FROM pages
                WHERE note_id = :note_id
            """), {
                'note_id': note_id
            }).fetchall()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return [{
            'page_id': page['id'],
            'title': page['title'],
            'keyword': page['keyword'],
            'content': page['content'],
            'note_id': page['note_id'],
            'created_at': page['created_at'],
            'updated_at': page['updated_at']
        } for page in page_list]

    def find_note_id_by_page_id(self, page_id: int) -> int:
        """페이지 id로 노트 id를 조회합니다.
        만약 페이지 정보가 존재하지 않으면 -1을 반환하고,
        에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param page_id: 조회할 페이지 id
        :return: 노트 id
        """
        try:
            row = self.db.execute(text("""
                SELECT
                    note_id
                FROM pages
                WHERE id = :page_id
            """), {
                'page_id': page_id
            }).fetchone()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return row['note_id'] if row else -1

    def find_page_owner_id_by_page_id(self, page_id: int) -> int:
        """페이지 id로 노트의 소유주(사용자) id를 조회합니다.
        만약 페이지 정보가 존재하지 않으면 -1을 반환하고,
        에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param page_id: 조회할 페이지 id
        :return: 사용자 id
        """
        try:
            row = self.db.execute(text("""
                SELECT
                    notes.user_id
                FROM pages
                INNER JOIN notes ON pages.note_id = notes.id
                WHERE pages.id = :page_id
            """), {
                'page_id': page_id
            }).fetchone()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return row['user_id'] if row else -1

    def find_page_id_and_keyword_by_note_id(self, note_id: int) -> list:
        """노트 id로 노트 안에 있는 모든 페이지 id와 키워드를 조회합니다.
        에러가 발생하면 'Runtime Error' 예외가 발생합니다.
        
        :param note_id: 조회할 노트 id
        :return: 페이지 id와 키워드를 포함한 리스트: 
            [{
                'page_id': int, # 페이지 id
                'keyword': str  # 키워드
            }]
        """
        try:
            page_list = self.db.execute(text("""
                SELECT
                    id,
                    keyword
                FROM pages
                WHERE note_id = :note_id
            """), {
                'note_id': note_id
            }).fetchall()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return [{
            'page_id': page['id'],
            'keyword': page['keyword']
        } for page in page_list]


    # update
    def update_page_header(self, page: dict) -> bool:
        """ 페이지 제목, 키워드를 수정합니다.
        그리고 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param page: 수정할 페이지 정보를 포함한 딕셔너리:
            {
                'page_id': int, # 페이지 id
                'title': str,   # 페이지 제목
                'keyword': str  # 페이지 키워드
            }
        :return: 수정 성공 여부 (True/False)
        """
        try:
            updated_rowcnt = self.db.execute(text("""
                UPDATE pages
                SET
                    title = :title,
                    keyword = :keyword
                WHERE id = :page_id
            """), {
                'title': page['title'],
                'keyword': page['keyword'],
                'page_id': page['page_id']
            }).rowcount
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return updated_rowcnt and updated_rowcnt > 0

    def update_page_content(self, page: dict) -> bool:
        """페이지 내용을 수정합니다.
        그리고 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param page: 수정할 페이지 정보를 포함한 딕셔너리:
            {
                'page_id': int, # 페이지 id
                'content': str  # 페이지 내용
            }
        :return: 수정 성공 여부 (True/False)
        """
        try:
            updated_rowcnt = self.db.execute(text("""
                UPDATE pages
                SET content = :content
                WHERE id = :page_id
            """), {
                'content': page['content'],
                'page_id': page['page_id']
            }).rowcount
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return updated_rowcnt and updated_rowcnt > 0


    # delete
    def delete_page_info(self, page_id) -> bool:
        """페이지 정보를 삭제합니다.
        그리고 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param page_id: 삭제할 페이지 id
        :return: 삭제 성공 여부 (True/False)
        """
        try:
            deleted_rowcnt = self.db.execute(text("""
                DELETE FROM pages
                WHERE id = :page_id
            """), {
                'page_id': page_id
            }).rowcount
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return deleted_rowcnt and deleted_rowcnt > 0
