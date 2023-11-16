class TrackPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'proxy_more' in request.path:
            print(request.path)

        response = self.get_response(request)
        return response
