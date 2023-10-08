def create_endpoint(app, services):

    # health check endpoint
    @app.route('/ping', methods=['GET'])
    def ping():
        return 'pong'
