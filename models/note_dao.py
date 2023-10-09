from sqlalchemy import text

class NoteDao:
    def __init__(self, database):
        self.db = database


    # create
    def insert_note_info(self, note: dict) -> int:
        """사용자 id와 노트의 제목, 설명, 접근 권한으로 노트를 생성합니다.
        그리고 노트 id를 반환합니다.
        만약 에러가 발생하면 None을 반환합니다.

        :param note: 생성할 노트 정보를 포함한 딕셔너리:
            {
                'user_id': int,             # 사용자 id
                'title': str,               # 노트 제목
                'description': str,         # 노트 설명
                'shared_permission': int    # 노트 접근 권한
            }
        :return: 생성된 노트 id
        """
        try:
            note_id = self.db.execute(text("""
                INSERT INTO notes (
                    title,
                    description,
                    user_id,
                    shared_permission
                ) VALUES (
                    :title,
                    :description,
                    :user_id,
                    :shared_permission
                )
            """), note).lastrowid
        except Exception as e:
            return None

        return note_id if note_id else None


    # read
    def get_note_info(self, note_id: int) -> dict:
        """노트 id로 노트 정보를 조회합니다.
        만약 노트 정보가 존재하지 않거나 에러가 발생하면 None을 반환합니다.

        :param note_id: 조회하려는 노트 id
        :return: 노트 정보가 포함된 딕셔너리:
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
            note = self.db.execute(text("""
                SELECT
                    id,
                    title,
                    description,
                    shared_permission,
                    user_id,
                    created_at,
                    updated_at
                FROM notes
                WHERE id = :note_id
            """), {
                'note_id': note_id
            }).fetchone()
        except Exception as e:
            return None

        return {
            'note_id': note['id'],
            'title': note['title'],
            'description': note['description'],
            'shared_permission': note['shared_permission'],
            'created_at': note['created_at'],
            'updated_at': note['updated_at'],
            'user_id': note['user_id']
        } if note else None

    def get_note_list(self, user_id: int) -> list:
        """사용자 id로 사용자의 모든 노트 정보를 조회한다.
        만약 사용자의 노트 정보가 존재하지 않거나 에러가 발생하면 None을 반환한다.

        :param user_id: 조회할 사용자 id
        :return: 모든 노트 정보가 포함된 리스트:
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
            note_list = self.db.execute(text("""
                SELECT
                    id,
                    title,
                    description,
                    shared_permission,
                    user_id,
                    created_at,
                    updated_at
                FROM notes
                WHERE user_id = :user_id
            """), {
                'user_id': user_id
            }).fetchall()
        except Exception as e:
            return e

        return [{
            'note_id': note['id'],
            'title': note['title'],
            'description': note['description'],
            'shared_permission': note['shared_permission'],
            'user_id': note['user_id'],
            'created_at': note['created_at'],
            'updated_at': note['updated_at']
        } for note in note_list] if note_list else None

    def find_user_id_by_note_id(self, note_id: int) -> int:
        """노트 id로 해당 노트의 소유주(사용자) id를 찾습니다.
        만약 존재하지 않으면 -1을 반환하고, 에러가 발생하면 None을 반환합니다.

        :param note_id: 조회할 노트 id
        :return: 사용자 id
        """
        try:
            row = self.db.execute(text("""
                SELECT
                    user_id
                FROM notes
                WHERE id = :note_id
            """), {
                'note_id': note_id
            }).fetchone()
        except Exception as e:
            return None

        return row['user_id'] if row else -1

    def find_shared_permission_by_note_id(self, note_id: int) -> int:
        """노트 id로 해당 노트의 공유 권한을 조회합니다.
        만약 노트가 존재하지 않으면 -1을 반환하고, 에러가 발생하면 None을 반환합니다.

        :param note_id: 조회할 노트 id
        :return: 해당 노트의 공유 권한
        """
        try:
            row = self.db.execute(text("""
                SELECT
                    shared_permission
                FROM notes
                WHERE id = :note_id
            """), {
                'note_id': note_id
            }).fetchone()
        except Exception as e:
            return None

        return row['shared_permission'] if row else -1


    # update
    def update_note_info(self, note: dict) -> bool:
        """ 노트의 제목, 설명, 공유 권한을 수정합니다.
        그리고 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생했다면 None을 반환합니다.

        :param note: 수정할 노트 정보를 포함한 딕셔너리:
            {
                'note_id': int,             # 노트 id
                'title': str,               # 노트 제목
                'description': str,         # 노트 설명
                'shared_permission': int    # 노트 공유 권한
            }
        :return: 수정 성공 여부 (True/False)
        """
        try:
            updated_rowcnt = self.db.execute(text("""
                UPDATE notes
                SET
                    title = :title,
                    description = :description,
                    shared_permission = :shared_permission
                WHERE id = :note_id
            """), note).rowcount
        except Exception as e:
            return None

        return True if updated_rowcnt is not None and updated_rowcnt > 0 else False


    # delete
    def delete_note_info(self, note_id: int) -> bool:
        """노트 정보를 삭제합니다. 그리고 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생했다면 None을 반환합니다.

        :param note_id: 삭제할 노트 id
        :return: 삭제 성공 여부 (True/False)
        """
        try:
            deleted_rowcnt = self.db.execute(text("""
                DELETE FROM notes
                WHERE id = :note_id
            """), {
                'note_id': note_id
            }).rowcount
        except Exception as e:
            return None

        return True if deleted_rowcnt is not None and deleted_rowcnt > 0 else False
