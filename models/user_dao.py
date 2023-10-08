from sqlalchemy import text

class UserDao:
    def __init__(self, database):
        self.db = database


    # create
    def insert_user_info(self, user: dict) -> int:
        """사용자의 email, password, profile로 회원가입을 합니다.
        그리고 사용자 id를 반환합니다.
        만약 에러가 발생하면 None을 반환합니다.

        :param user: 생성하고자 하는 사용자 정보를 담고 있는 딕셔너리:
            {
                'email': str,       # 사용자의 이메일
                'password': str,    # 사용자의 비밀번호
                'profile': str      # 사용자의 프로필
            }
        :return: 생성된 사용자 id
        """
        try:
            user_id = self.db.execute(text("""
                INSERT INTO users (
                    email,
                    profile,
                    hashed_password
                ) VALUES (
                    :email,
                    :profile,
                    :password
            )"""), user).lastrowid
        except:
            return None

        return user_id if user_id else None


    # read
    def get_user_info(self, user_id: int) -> dict:
        """ 사용자 id로 password를 제외한 사용자의 정보를 조회합니다.
        만약 사용자 정보가 존재하지 않거나 에러가 발생하면 None을 반환합니다.

        :param user_id: 조회하려는 사용자 id
        :return: 사용자 정보가 포함된 딕셔너리:
            {
                'user_id': int,     # 사용자 id
                'email': str,       # 사용자의 이메일
                'profile': str,     # 사용자의 프로필
                'created_at': str,  # 사용자 정보 생성일
                'updated_at': str   # 사용자 정보 마지막 수정일
            }
        """
        try:
            user = self.db.execute(text("""
                SELECT
                    id,
                    email,
                    profile,
                    created_at,
                    updated_at
                FROM users
                WHERE id = :user_id
            """), {
                'user_id': user_id
            }).fetchone()
        except:
            user = None

        return {
            'user_id': user['id'],
            'email': user['email'],
            'profile': user['profile'],
            'created_at': user['created_at'],
            'updated_at': user['updated_at']
        } if user else None

    def find_user_id_by_email(self, email: str) -> int:
        """ 사용자의 email로 사용자 id를 찾습니다.
        만약 사용자 id가 존재하지 않으면 -1을 반환하고, 에러가 발생하면 None을 반환합니다.

        :param email: 사용자의 이메일
        :return: 사용자의 id
        """
        try:
            row = self.db.execute(text("""    
                SELECT
                    id
                FROM users
                WHERE email = :email
            """), {'email' : email}).fetchone()
        except:
            return None

        return row['id'] if row else -1

    def find_user_id_and_password_by_email(self, email: str) -> dict:
        """ 사용자의 이메일로 사용자 id와 비밀번호를 찾습니다.
        만약 사용자 정보가 존재하지 않거나 에러가 발생하면 None을 반환합니다.
        
        :param email: 사용자의 이메일
        :return: 사용자의 id와 비밀번호: 
            {
                'user_id': int,         # 사용자 id
                'hashed_password': str  # 사용자의 암호화된 비밀번호
            }
        """
        try:
            row = self.db.execute(text("""    
                SELECT
                    id,
                    hashed_password
                FROM users
                WHERE email = :email
            """), {'email' : email}).fetchone()
        except:
            row = None

        return {
            'user_id': row['id'],
            'hashed_password': row['hashed_password']
        } if row else None


    # update
    def update_user_info(self, user: dict) -> bool:
        """ 사용자의 프로필을 수정합니다. 그리고 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생했다면 None을 반환합니다.
        
        :param user: 수정할 사용자의 정보: 
            {
                'user_id': int, # 사용자 id
                'profile': str  # 사용자의 프로필
            }
        :return: 업데이트 성공 여부 (True, False)
        """
        try:
            updated_rowcnt = self.db.execute(text("""
                UPDATE users
                SET profile = :profile
                WHERE id = :user_id
            """), {
                'user_id': user['user_id'],
                'profile': user['profile']
            }).rowcount
        except:
            return None

        return True if updated_rowcnt is not None and updated_rowcnt > 0 else False


    # delete
    def delete_user_info(self, user_id: int) -> bool:
        """사용자 정보를 삭제합니다. 그리고 성공 여부(True/False)를 반환합니다.
        만약 에러가 발생했다면 None을 반환합니다.

        :param user_id: 삭제할 사용자 id
        :return: 삭제 성공 여부 (True, False)
        """
        try:
            deleted_rowcnt = self.db.execute(text("""
                DELETE FROM users
                WHERE id = :user_id
            """), {
                'user_id': user_id
            }).rowcount
        except:
            return None

        return True if deleted_rowcnt is not None and deleted_rowcnt > 0 else False
