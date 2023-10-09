from data import NoteMessage

class NoteService:
    def __init__(self, note_dao):
        self.note_dao = note_dao


    # verify
    def confirm_auth(self, user_id: int, note_id: int) -> bool:
        """사용자와 노트의 소유주(사용자)와 같은 사용자인지 비교합니다.
        만약 노트나 사용자가 존재하지 않거나 에러가 발생하면 NoteMessage를 반환합니다.

        :param user_id: 사용자 id
        :param note_id: 노트 id
        :return: 같은 사용자인지 (True/False)
        """
        try:
            note_owner_id = self.note_dao.find_user_id_by_note_id(note_id)
        except Exception as e:
            return NoteMessage.ERROR
        finally:
            if note_owner_id is None:
                return NoteMessage.ERROR
            elif note_owner_id == -1:
                return NoteMessage.FAIL_NOT_EXISTS

        return True if user_id == note_owner_id else False

    def confirm_note_permission(self, note_id: int) -> bool:
        """노트 접근 권한이 있는지 확인하고, 권한 여부(True/False)를 반환합니다.
        만약 노트 정보가 존재하지 않거나 에러가 발생하면 NoteMessage를 반환합니다.

        :param note_id: 확인할 note_id
        :return: 노트 접근 권한 여부 (True/False)
        """
        try:
            note_permission = self.note_dao.find_shared_permission_by_note_id(note_id)
        except Exception as e:
            return NoteMessage.ERROR
        finally:
            if note_permission is None:
                return NoteMessage.ERROR
            elif note_permission == -1:
                return NoteMessage.FAIL_NOT_EXISTS

        return False if note_permission == 1 else True


    # create
    def create_new_note(self, new_note: dict) -> int:
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
    def get_user_chosen_note(self, note_id: int) -> dict:
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


    def get_list_of_user_note(self, user_id: int) -> list:
        """사용자 id로 사용자의 노트 목록을 조회합니다.
        만약 노트 목록이 존재하지 않거나 에러가 발생하면 NoteMessage를 반환합니다.

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

        return note_list if note_list else NoteMessage.FAIL_NOT_EXISTS
    # update
    def update_note(self, note: dict) -> str:
        """노트의 제목, 설명, 공유 권한 받아 노트 정보를 수정합니다.
        그리고 수정된 날짜를 반환합니다.
        만약 수정에 실패하거나 에러가 발생하면 NoteMessage를 반환합니다.

        :param note: 노트 정보가 포함된 딕셔너리
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
        except Exception as e:
            return NoteMessage.ERROR
        finally:
            if not is_updated:
                return NoteMessage.ERROR

        try:
            updated_note = self.note_dao.get_note_info(note['note_id'])
        except Exception as e:
            return NoteMessage.ERROR

        return updated_note['updated_at'] if updated_note else NoteMessage.ERROR


    # delete
    def delete_note(self, note_id: int) -> bool:
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

        return is_deleted if is_deleted is not None else NoteMessage.ERROR
