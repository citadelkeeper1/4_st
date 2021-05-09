import quopri
from .requester import GetReqs, PostReqs


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', 'Ошибка 404: страница не найдена.'


class Framework:
    def __init__(self, routes, fronts):
        self.routes_lst = routes
        self.fronts_lst = fronts

    def __call__(self, environment, start_response):
        path = environment['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        method = environment['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostReqs().get_parameters(environment)
            request['data'] = data
            print(f'POST REQUEST detected: {Framework.decode_value(data)}')

        if method == 'GET':
            request_params = GetReqs().get_parameters(environment)
            request['request_params'] = request_params
            print(f'GET REQUEST detected: {request_params}')

        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()
        # request = {}
        for front in self.fronts_lst:
            front(request)
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            new_data[k] = quopri.decodestring(val).decode('UTF-8')
        return new_data


class DebugApplication(Framework):
    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        print('DEBUG MODE')
        print(env)
        return self.application(env, start_response)


class FakeApplication(Framework):
    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
