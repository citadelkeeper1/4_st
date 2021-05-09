from time import time


class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kw):
                time_start = time()
                result = method(*args, **kw)
                time_end = time()
                running_time = time_end - time_start
                print(f'(debug info) {self.name} [running time: {running_time:2.2f} ms]')
                return result
            return timed
        return timeit(cls)
