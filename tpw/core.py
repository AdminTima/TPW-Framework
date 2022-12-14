

class Tpw:

    def __call__(self, eniron, start_response):
        status = "200 OK"
        resp = b"Hello world class"
        start_response(status, headers=[])
        yield resp
