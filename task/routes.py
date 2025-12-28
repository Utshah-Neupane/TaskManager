from task import app


@app.route("/")
@app.route("/home")
def home_page():
    return "Hello World"
    