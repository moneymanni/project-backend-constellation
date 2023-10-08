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
    FAIL_EMAIL_ALREADY_EXISTS = '[user] 이미 존재하는 이메일'
    FAIL_NOT_EMAIL = '[user] 유효 하지 않은 이메일'
    ERROR = '[user] 요청 중 오류 발생'
