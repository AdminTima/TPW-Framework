from webob import Request, Response
from parse import parse
import inspect
import os
from jinja2 import Environment, FileSystemLoader
from whitenoise import WhiteNoise
from waitress import serve


class BaseApp:

    def __init__(self):
        self._routes = {}

    def route(self, path, methods=None):
        def wrapper(handler):
            self.add_route(path, handler, methods)
            print(self._routes)
            return handler

        return wrapper

    def add_route(self, path, handler, methods=None):
        if path in self._routes:
            raise Exception(f"Route {path} is already registered!")
        if methods is None:
            methods = ["GET"]
        new_route = {"handler": handler, "methods": methods}
        self._routes[path] = new_route

    @property
    def routes(self):
        return self._routes


class Tsunami(BaseApp):

    def __init__(self, templates_dir="templates", static_dir=None):
        super().__init__()
        self.template_env = Environment(loader=FileSystemLoader(os.path.abspath(templates_dir)))
        self.static_dir = static_dir
        self.white_noise = WhiteNoise(self.__wsgi_app, root=static_dir)

    def __wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        path_info: str = environ["PATH_INFO"]
        if path_info.startswith("/static"):
            environ["PATH_INFO"] = path_info[len("/static"):]
            if self.static_dir:
                return self.white_noise(environ, start_response)
            raise Exception("You have not provided static directory")
        return self.__wsgi_app(environ, start_response)

    def handle_request(self, request):
        response = Response()
        handler, kwargs = self.find_handler(request.path, request.method)

        if handler is None:
            return self.not_found_response(response)

        if inspect.isclass(handler):
            req_method = request.method.lower()
            handler = getattr(handler(), req_method, None)
            if not handler:
                raise Exception("Method not allowed.")

        response = handler(request, response, **kwargs)
        return response

    def find_handler(self, request_path, request_method):
        for path in self._routes:
            parsed_result = parse(path, request_path)
            if parsed_result:
                route_handler_data = self._routes[path]
                if request_method in route_handler_data["methods"]:
                    return route_handler_data["handler"], parsed_result.named
                return self.__method_not_allowed, dict()

        return None, None

    def not_found_response(self, response):
        response.text = "Not found page"
        response.status_code = 404
        return response

    def render_template(self, template_name, context=None):
        if context is None:
            context = {}
        template = self.template_env.get_template(template_name)
        print(template)
        return template.render(**context).encode("utf-8")

    def __method_not_allowed(self,request, response):
        response.text = "Method not allowed."
        response.status_code = 405
        return response

    def include_router(self, router):
        if not isinstance(router, Router):
            raise Exception("Router has to be an instance of Router class")
        self._routes.update(router.routes)
        print(self._routes)

    def run(self):
        serve(self)



class Router(BaseApp):
    pass

