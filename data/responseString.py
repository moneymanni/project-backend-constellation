from enum import Enum


class ResponseText(Enum):
    SUCCESS = 'success'
    FAIL = 'fail'
    PERMISSION_DENIED = '잘못된 접근'


class IndexMessage(Enum):
    SUCCESS = '[index] 요청 처리 완료'
    ERROR = '[index] 요청 오류 발생'


class JwtMessage(Enum):
    FAIL_NOT_INVALID = '[jwt] 유효하지 않는 토큰'
    FAIL_NOT_EXISTS = '[jwt] 존재하지 않는 토큰'
    ERROR = '[jwt] 요청 오류 발생'


class AuthMessage(Enum):
    LOGIN = '[auth] 로그인 완료'
    LOGOUT = '[auth] 로그아웃 완료'
    FAIL_IS_LOGIN = '[auth] 로그인 실패'
    FAIL_IS_LOGOUT = '[auth] 로그아웃 실패'
    FAIL_NOT_PERMISSION = '[auth] 권한 없음'
    FAIL_NOT_MATCH = '[auth] 사용자 정보가 일치하지 않음'
    FAIL_NOT_EXISTS = '[auth] 사용자 정보가 존재하지 않음'
    ERROR = '[auth] 요청 중 오류 발생'


class UserMessage(Enum):
    CREATE = '[user] 사용자 정보 추가 완료'
    READ = '[user] 사용자 정보 조회 완료'
    UPDATE = '[user] 사용자 정보 수정 완료'
    DELETE = '[user] 사용자 정보 삭제 완료'
    GET = '[user] 사용자 정보 요청 완료'
    FAIL_NOT_USER = '[user] 존재 하지 않는 사용자'
    FAIL_EMAIL_ALREADY_EXISTS = '[user] 이미 존재하는 이메일'
    FAIL_NOT_EMAIL = '[user] 유효 하지 않은 이메일'
    ERROR = '[user] 요청 중 오류 발생'

class NoteMessage(Enum):
    CREATE = '[note] 노트 정보 추가 완료'
    READ = '[note] 노트 정보 조회 완료'
    UPDATE = '[note] 노트 정보 수정 완료'
    DELETE = '[note] 노트 정보 삭제 완료'
    GET = '[note] 노트 정보 요청 완료'
    FAIL_NOT_PERMISSION = '[note] 노트 접근 권한 없음'
    FAIL_NOT_EXISTS = '[note] 존재하지 않는 노트'
    ERROR = '[note] 요청 중 오류 발생'

class PageMessage(Enum):
    CREATE = '[page] 페이지 정보 추가 완료'
    READ = '[page] 페이지 정보 조회 완료'
    UPDATE = '[page] 페이지 정보 수정 완료'
    DELETE = '[page] 페이지 정보 삭제 완료'
    GET = '[page] 페이지 정보 요청 완료'
    FAIL_NOT_PERMISSION = '[page] 페이지 접근 권한 없음'
    FAIL_NOT_EXISTS = '[page] 존재하지 않는 페이지'
    FAIL_NOT_SAME_NOTE = '[page] 두 페이지가 같은 노트에 포함되지 않음'
    ERROR = '[page] 요청 중 오류 발생'

class LinkMessage(Enum):
    CREATE = '[link] 페이지 간 연결 정보 추가 완료'
    READ = '[link] 페이지 간 연결 정보 조회 완료'
    UPDATE = '[link] 페이지 간 연결 정보 수정 완료'
    DELETE = '[link] 페이지 간 연결 정보 삭제 완료'
    GET = '[link] 페이지 간 연결 정보 요청 완료'
    FAIL_IS_INCLUDED_IN_DIFFERENT_NOTE = '[link] 노트가 다름'
    FAIL_NOT_PERMISSION = '[link] 접근 권한 없음'
    FAIL_IS_EXISTS = '[link] 이미 존재하는 연결입니다.'
    ERROR = '[link] 요청 중 오류 발생'

class TagMessage(Enum):
    CREATE = '[tag] 태그 정보 추가 완료'
    READ = '[tag] 태그 정보 조회 완료'
    UPDATE = '[tag] 태그 정보 수정 완료'
    DELETE = '[tag] 태그 정보 삭제 완료'
    FAIL_IS_EXISTS = '[tag] 이미 존재하는 태그입니다.'
    FAIL_NOT_EXISTS = '[tag] 존재하지 않는 태그입니다.'
    ERROR = '[tag] 요청 중 오류 발생'

class VisualizationMessage(Enum):
    READ = '[visualization] 시각화 정보 조회 완료'
    ERROR = '[visualization] 요청 중 오류 발생'

class RecommendMessage(Enum):
    GET = '[recommend] 요청 완료'
    ERROR = '[recommend] 요청 중 오류 발생'
