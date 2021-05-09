class PostReqs:
    @staticmethod
    def get_input_dict(data: str):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                key, val = item.split('=')
                result[key] = val
        return result

    @staticmethod
    def read_wsgi_input(env) -> bytes:
        if not env.get('CONTENT_LENGTH'):
            return b''
        return env['wsgi.input'].read(int(env.get('CONTENT_LENGTH')))

    def parse_wsgi_input(self, data: bytes) -> dict:
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.get_input_dict(data_str)
        return result

    def get_parameters(self, environment):
        data = self.read_wsgi_input(environment)
        data = self.parse_wsgi_input(data)
        return data


class GetReqs:
    @staticmethod
    def get_input_dict(data: str):
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_parameters(environment):
        query_string = environment['QUERY_STRING']
        request_params = GetReqs.get_input_dict(query_string)
        return request_params
