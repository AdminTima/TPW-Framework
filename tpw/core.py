from webob import Request, Response
from parse import parse
import inspect


class Tpw:

    def __init__(self):
        self.__routes = {}

    def __call__(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request.path)

        if handler is None:
            return self.not_found_response(response)

        if inspect.isclass(handler):
            req_method = request.method.lower()
            handler = getattr(handler(), req_method, None)
            if not handler:
                raise Exception("Method not allowed.")

        response.text = handler(request, **kwargs)
        return response

    def find_handler(self, request_path):
        for path, handler in self.__routes.items():
            parsed_result = parse(path, request_path)
            if parsed_result:
                return handler, parsed_result.named

        return None, None

    def route(self, path):

        def wrapper(handler):
            self.add_route(path, handler)
            print(self.__routes)
            return handler
        return wrapper

    def add_route(self, path, handler):
        if path in self.__routes:
            raise Exception(f"Route {path} is already registered!")
        self.__routes[path] = handler


    def not_found_response(self, response):
        response.text = "Not found page"
        response.status_code = 404
        return response


