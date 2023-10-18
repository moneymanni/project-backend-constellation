from sqlalchemy import text
from typing import Optional

class TagDao:
    def __init__(self, database):
        self.db = database

    # create
    def insert_tag_info(self, tag: dict) -> int:
        """태그 정보를 받아 태그를 생성합니다.
        그리고 태그 id를 반환합니다.
        만약 태그 정보 생성에 실패하면 -1을 반환하고,
        에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param tag: 생성할 태그 정보를 퐇마한 딕셔너리:
            {
                'name': str,    # 태그명
                'note_id': int  # 노트 id
            }
        :return: 생성된 태그 id
        """
        try:
            tag_id = self.db.execute(text("""
                INSERT INTO tags (
                    name,
                    note_id
                ) VALUES (
                    :name,
                    :note_id
                )
            """), {
                'name': tag['name'],
                'note_id': tag['note_id']
            }).lastrowid
        except Exception as e:
            raise RuntimeError('Database Error') from e

        return tag_id if tag_id else -1

    def insert_page_tag_list_info(self, page_tag_info: dict) -> bool:
        """페이지 id와 태그 id를 받아 페이지-태그 리스트 정보를 생성합니다.
        그리고 생성 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param page_tag_info: 페이지와 태그 정보를 포함한 딕셔너리:
            {
                'page_id': int, # 페이지 id
                'tag_id': int   # 태그 id
            }
        :return: 생성 성공 여부 (True/False)
        """
        try:
            created_rowcnt = self.db.execute(text("""
                INSERT INTO page_tag_list (
                    page_id,
                    tag_id
                ) VALUES (
                    :page_id,
                    :tag_id
                )
            """), {
                'page_id': page_tag_info['page_id'],
                'tag_id': page_tag_info['tag_id']
            }).rowcount
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return created_rowcnt and created_rowcnt > 0

    # read
    def get_tag_info(self, tag_id: int) -> Optional[dict]:
        """태그 id로 태그 정보를 조회합니다.
        만약 태그 정보가 존재하지 않으면 None을 반환하고,
        에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param tag_id: 조회할 태그 id
        :return: 태그 정보가 포함된 딕셔너리:
            {
                'tag_id': int,  # 태그 id
                'name': str,    # 태그명
                'note_id': int  # 노트 id
            }
        """
        try:
            tag = self.db.execute(text("""
                SELECT
                    id,
                    name,
                    note_id
                FROM tags
                WHERE id = :tag_id
            """), {
                'tag_id': tag_id
            }).fetchone()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return {
            'tag_id': tag['id'],
            'name': tag['name'],
            'note_id': tag['note_id']
        } if tag else None

    def find_tag_list_by_page_id(self, page_id: int) -> list:
        """페이지 id로 페이지에 포함된 모든 태그 정보를 조회합니다.
        만약 태그 정보가 존재하지 않으면 빈 리스트를 반환하고,
        에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param page_id: 조회할 페이지 id
        :return: 모든 태그 정보가 포함된 리스트:
            [{
                'tag_id': int,  # 태그 id
                'name': str,    # 태그명
                'note_id': int  # 노트 id
            }]
        """
        try:
            tag_list = self.db.execute(text("""
                SELECT
                    tags.note_id AS note_id,
                    tags.id AS tag_id,
                    tags.name
                FROM pages
                JOIN page_tag_list ON pages.id = page_tag_list.page_id
                JOIN tags ON tags.id = page_tag_list.tag_id
                WHERE pages.id = :page_id
            """), {
                'page_id': page_id
            }).fetchall()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return [{
            'note_id': tag['note_id'],
            'tag_id': tag['tag_id'],
            'name': tag['name']
        } for tag in tag_list]

    def find_tag_list_by_note_id(self, note_id: int) -> list:
        """노트 id로 노트에 포함된 모든 태그 정보를 조회합니다.
        만약 태그 정보가 존재하지 않으면 빈 리스트를 반환하고,
        에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param note_id: 조회할 노트 id
        :return: 모든 태그 정보가 포함된 리스트:
            [{
                'tag_id': int,  # 태그 id
                'name': str,    # 태그명
                'note_id': int  # 노트 id
            }]
        """
        try:
            tag_list = self.db.execute(text("""
                SELECT
                    id,
                    name,
                    note_id
                FROM tags
                WHERE note_id = :note_id
            """), {
                'note_id': info['note_id']
            }).fetchall()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return [{
            'note_id': tag['note_id'],
            'tag_id': tag['id'],
            'name': tag['name']
        } for tag in tag_list]

    def find_tag_id_by_tag_name_and_note_id(self, tag: dict) -> int:
        """태그명과 노트 id로 태그 id를 조회합니다.
        만약 태그가 존재하지 않으면 -1을 반환하고,
        에러가 발새하면 'Runtime Error' 예외가 발생합니다.

        :param tag: 태그명과 노트 id를 포함한 딕셔너리:
            {
                'name': str,    # 태그명
                'note_id': int  # 노트 id
            }
        :return: 태그 id
        """
        try:
            row = self.db.execute(text("""
                SELECT
                    id
                FROM tags
                WHERE name = :name
                AND note_id = :note_id
            """), {
                'name': tag['name'],
                'note_id': tag['note_id']
            }).fetchone()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return row['id'] if row else -1

    def find_page_tag_list_by_tag_id(self, tag_id: int) -> list:
        """태그 id로 모든 페이지-태그 리스트를 조회합니다.
        만약 페이지-태그 리스트 정보가 존재하지 않으면 빈 리스트를 반환하고,
        에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param tag_id: 조회할 태그 id
        :return: 모든 페이지-태그 리스트 정보를 포함한 리스트:
            [{
                'page_id': int, # 페이지 id
                'tag_id': int   # 태그 id
            }]
        """
        try:
            page_tag_list = self.db.execute(text("""
                SELECT
                    page_id,
                    tag_id
                FROM page_tag_list
                WHERE tag_id = :tag_id
            """), {
                'tag_id': tag_id
            }).fetchall()
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return [{
            'page_id': page_tag['page_id'],
            'tag_id': page_tag['tag_id'],
        } for page_tag in page_tag_list]


    # update
    def update_tag_info(self, tag: dict) -> bool:
        """태그 정보를 수정합니다.
        그리고 수정 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param tag: 수정할 태그 정보를 포함한 딕셔너리:
            {
                'tag_id': int,  # 태그 id
                'name': str     # 태그명
            }
        :return: 수정 성공 여부 (True/False)
        """
        try:
            updated_rowcnt = self.db.execute(text("""
                UPDATE tags
                SET name = :name
                WHERE id = :tag_id
            """), {
                'tag_id': tag['tag_id'],
                'name': tag['name']
            }).rowcount
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return updated_rowcnt and updated_rowcnt > 0


    # delete
    def delete_tag_info(self, tag_id: int) -> bool:
        """태그 정보를 삭제합니다.
        그리고 삭제 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param tag_id: 삭제할 태그 id
        :return: 삭제 성공 여부 (True/False)
        """
        try:
            deleted_rowcnt = self.db.execute(text("""
                DELETE FROM tags
                WHERE id = :tag_id
            """), {
                'tag_id': tag_id
            }).rowcount
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return deleted_rowcnt and deleted_rowcnt > 0

    def delete_page_tag_list_info(self, page_tag_info: dict) -> bool:
        """페이지와 태그 id로 페이지-태그 정보를 삭제합니다.
        그리고 삭제 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생하면 'Runtime Error' 예외가 발생합니다.

        :param page_tag_info: 페이지와 태그 정보가 포함된 딕셔너리:
            {
                'page_id': int, # 페이지 id
                'tag_id': int   # 태그 id
            }
        :return: 삭제 성공 여부 (True/False)
        """
        try:
            deleted_rowcnt = self.db.execute(text("""
            DELETE FROM page_tag_list
            WHERE page_id = :page_id
            AND tag_id = :tag_id
        """), {
            'page_id': info['page_id'],
            'tag_id': info['tag_id']
        }).rowcount
        except Exception as e:
            raise RuntimeError("Database Error") from e

        return deleted_rowcnt and deleted_rowcnt > 0
