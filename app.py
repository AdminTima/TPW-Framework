from waitress import serve
from tsunami.core import Tsunami

app = Tsunami()


@app.route("/")
def home(request, response):
    response.text = "Hello home page"
    return response


@app.route("/hello/{name}")
def hello(request, response, name):
    response.text = f"Hello {name}"
    return response


@app.route("/about")
def about(request, response):
    response.text = "Hello about page"
    return response


@app.route("/class")
class ClassBased:
    def get(self, request, response):
        response.text = "Class based.."
        return response


def dj_like(request, response):
    response.text = "Route like django"
    return response


@app.route("/temp")
def template_test(request, response):
    response.body = app.render_template("index.html", {"name": "Tim"})
    return response


app.add_route("/dj", dj_like)


if __name__ == "__main__":
    serve(app)
