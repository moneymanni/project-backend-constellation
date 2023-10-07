def response_from_message(state: str, message: str, *args: any):
    """ 상태, 메시지, 데이터를 반환한다.

    :param state: 상태
    :param message: 메시지
    :param args: 데이터
    :return: 상태와 메시지, 데이터를 반환
    """
    response_message = {
        'state': state,
        'message': message
    }
    if args:
        response_message['data'] = args[0]

    return response_message
