from flask import *
from random import randrange

app = Flask(__name__)


# =====================================
# basic routes
# =====================================
@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello():
    return 'Hello, World'


@app.route('/count/<to>')
def count(to):
    s = 'Count to ' + to + ": "
    for i in range(1, int(to) + 1):
        s += str(i) + " "
    return s


@app.route("/header")
def headers():
    return request.headers['Accept-Language']


# =====================================
# template demos
# =====================================

@app.route("/template")
def template():
    return render_template("demo.html.jinja")


@app.route("/template/loop")
def template_loop():
    return render_template("loop.html.jinja")


@app.route("/template/base/1")
def template_base1():
    return render_template("extends1.html.jinja")


@app.route("/template/base/2")
def template_base2():
    return render_template("extends2.html.jinja")


# =====================================
# form demos
# =====================================

@app.get("/form")
def form():
    return render_template("form.html.jinja")


@app.post("/form")
def form_post():
    form_data = request.form["form_data"]
    return render_template("form.html.jinja",
                           form_data=form_data)


@app.route("/form/prg", methods=["POST", "GET"])
def prg():
    if request.method == "POST":
        form_data = request.form["form_data"]  # ignore for now
        session['form_data'] = form_data
        return redirect("/form/prg")
    else:
        form_data = session.pop("form_data", None)
        return render_template("prg.html.jinja", form_data=form_data)


app.secret_key = "3974c04332e8d15fa74080740400038783d106ff695ce77df86456992a531e2f"


@app.route("/form/session", methods=["POST", "GET"])
def session_demo():
    if request.method == "POST":
        form_data = request.form["form_data"]
        session['form_data'] = form_data
        return redirect("/form/session")
    else:
        return render_template("session.html.jinja",
                               form_data=session.pop('form_data', None))


@app.route("/cookie")
def cookie():
    print("Cookie: " + str(request.cookies.get("CSCI-491")))
    response = make_response("Cookie set!")
    val = "Is Pretty Cool..." + str(randrange(100))
    response.set_cookie("CSCI-491", val)
    return response
