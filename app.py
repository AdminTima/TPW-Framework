from waitress import serve
from tpw.core import Tpw

app = Tpw()


@app.route("/")
def home(request):
    return "Hello home page"


@app.route("/hello/{name}")
def hello(request, name):
    return f"Hello {name}"


@app.route("/about")
def about(request):
    return "Hello about page"


@app.route("/class")
class ClassBased:
    def get(self, request):
        return "Class based view works!!!!"


def dj_like(request):
    return "Route like django"


app.add_route("/dj", dj_like)


if __name__ == "__main__":
    serve(app)
