from tsunami.core import Tsunami, Router
from tsunami.serializer import TsunamiSerializer


app = Tsunami(static_dir="static")
router = Router(prefix="/auth")


@router.route("/router-test")
def router_test(req, res):
    res.text = "Router is working ......!!!!!"
    return res


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


class User:
    username: str
    password: str

    def __init__(self, username, password):
        self.username = username
        self.password = password


@router.route("/serializer", methods=["GET", "POST"])
def serializer_test(req, res):
    if req.method == "POST":
        result = TsunamiSerializer().deserialize(req.body, to_instance=User)
        print(result.__dict__)
        res.text = "success"
        return res
    obj = User("Tim", "swordfish")
    res.headerlist = [('Content-Type', 'application/json')]
    res.text = TsunamiSerializer().serialize(obj)
    return res


app.add_route("/dj", dj_like)
app.include_router(router)


if __name__ == "__main__":
    app.run()
