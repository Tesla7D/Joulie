from eve import Eve

app = Eve()


@app.route("/")
def index():
    return "Index"


@app.route("/x")
def default():
    return "Default"


@app.route("/hello", methods=['GET'])
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(port=1337, debug=True)
