from flask import Blueprint, request, jsonify, g
import json

from data import response_from_message, ResponseText, UserMessage
from forms import SignUpForm, UserInfoUpdateForm

def create_user_endpoint(services, config):
    user_view = Blueprint('user_view', __name__)

    user_service = services.user_service
    jwt_service = services.jwt_service

    # create
    @user_view.route('/sign-up', methods=['POST'])
    def user_sign_up():
        """회원가입 엔드포인트

        :request 회원가입하는 사용자의 정보가 담긴 json 객체:
            {
                "email": str,       # 사용자의 이메일
                "password": str,    # 사용자의 비밀번호
                "profile": str      # 사용자의 프로필
            }
        :response 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "accessToken": str,     # access 토큰
                "tokenExpiration": int, # 토큰 유효 기간
                "state": str,           # 상태
                "message": str,         # 결과 메시지
                "data": {               # 반환하는 데이터
                        userId: str     # 가입한 사용자 id
                }
            }
        """
        form = SignUpForm(meta={"csrf": False})
        if not form.validate():
            return json.dumps(form.errors), 400

        body = request.json
        new_user = {
            'email': body['email'],
            'password': body['password'],
            'profile': body['profile']
        }

        try:
            new_user_id = user_service.create_new_user(new_user)

            if isinstance(new_user_id, UserMessage):
                message = response_from_message(ResponseText.FAIL.value, new_user_id.value)
                if new_user_id == UserMessage.FAIL_EMAIL_ALREADY_EXISTS:
                    return jsonify(message), 400
                return jsonify(message), 500

            access_token = jwt_service.generate_access_token(new_user_id)
            access_token_exp = config['JWT_EXP_DELTA_SECONDS']
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, UserMessage.ERROR.value)), 500

        user = response_from_message(ResponseText.SUCCESS.value, UserMessage.CREATE.value, {'userId': new_user_id})
        user['accessToken'], user['tokenExpiration'] = access_token, access_token_exp

        return jsonify(user), 201


    # read
    @user_view.route('', methods=['GET'])
    @jwt_service.login_required
    def user():
        """사용자 정보 조회 엔드포인트

        :request access token이 담긴 헤더:
            {
                "accessToken": str      # 사용자의 access 토큰
            }
        :response 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,               # 상태
                "message": str,             # 결과 메시지
                "data": {                   # 반환하는 데이터
                        "userId": str,      # 사용자 id
                        "email": str,       # 사용자의 이메일
                        "profile": str,     # 사용자의 프로필
                        "createdAt": str,   # 사용자의 등록일
                        "updatedAt": str    # 사용자 정보 마지막 수정일
                    }
            }
        """
        try:
            user = user_service.get_user(g.user_id)

            if isinstance(user, UserMessage):
                message = response_from_message(ResponseText.FAIL.value, user.value)
                if user == UserMessage.FAIL_NOT_USER:
                    return jsonify(message), 400
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, UserMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, UserMessage.READ.value, {
            'userId': user['user_id'],
            'email': user['email'],
            'profile': user['profile'],
            'createdAt': user['created_at'],
            'updatedAt': user['updated_at']
        })),200


    # update
    @user_view.route('/update', methods=['POST'])
    @jwt_service.login_required
    def user_update():
        """사용자 정보 수정 엔드포인트

        :request access token이 담긴 헤더:
            {
                "accessToken": str      # 사용자의 access 토큰
            }
        :request 수정할 사용자 정보가 담긴 json 객체:
            {
                "profile": str  # 사용자 프로필
            }
        :response 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,               # 상태
                "message": str,             # 결과 메시지
                "data": {                   # 반환하는 데이터
                        "updatedAt": str    # 사용자 정보 마지막 수정일
                    }
            }
        """
        form = UserInfoUpdateForm(meta={"csrf": False})
        if not form.validate():
            return json.dumps(form.errors), 400

        body = request.json
        user = {
            'user_id': g.user_id,
            'profile': body['profile']
        }

        try:
            updated_user = user_service.update_user(user)

            if isinstance(updated_user, UserMessage):
                message = response_from_message(ResponseText.FAIL.value, updated_user.value)
                return jsonify(message), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, UserMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, UserMessage.UPDATE.value, {'updatedAt': updated_user})), 200


    # delete
    @user_view.route('/leave', methods=['POST'])
    @jwt_service.login_required
    def user_leave():
        """회원탈퇴 엔드포인트

        :request access token이 담긴 헤더:
            {
                "accessToken": str      # 사용자의 access 토큰
            }
        :response 상태, 결과메시지, 데이터가 담긴 json 객체:
            {
                "state": str,               # 상태
                "message": str,             # 결과 메시지
            }
        """

        try:
            deleted_user = user_service.delete_user(g.user_id)

            if isinstance(deleted_user, UserMessage):
                message = response_from_message(ResponseText.FAIL.value, deleted_user.value)
                return jsonify(message), 500
            elif not deleted_user:
                return jsonify(response_from_message(ResponseText.FAIL.value, UserMessage.ERROR.value)), 500
        except Exception as e:
            return jsonify(response_from_message(ResponseText.FAIL.value, UserMessage.ERROR.value)), 500

        return jsonify(response_from_message(ResponseText.SUCCESS.value, UserMessage.DELETE.value)), 200


    return user_view
