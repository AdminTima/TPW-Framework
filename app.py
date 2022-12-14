from waitress import serve
from tpw.core import Tpw

app = Tpw()


if __name__ == "__main__":
    serve(app)
