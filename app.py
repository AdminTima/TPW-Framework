from waitress import serve
from tpw.core import Tpw

app = Tpw()


@app.route("/")
def home(request):
    return "Hello home page"


@app.route("/about")
def about(request):
    return "Hello about page"


if __name__ == "__main__":
    serve(app)
