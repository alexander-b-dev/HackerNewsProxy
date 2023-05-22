from flask import Flask, make_response, request
import config
import requests
from parser import AddTM


def create_app():
    app = Flask(__name__, static_folder=r'static')
    app.config['DEBUG'] = config.debug
    app.config['SECRET_KEY'] = config.key

    @app.route('/')
    @app.route('/<reqPath>', methods=["GET", "POST"])
    def index(reqPath=""):  # unused arg for compatibility
        try:
            if request.method == "GET":  # for vast majority requests
                data = requests.get(request.url.replace(request.host_url, config.originURL),
                                    cookies=request.cookies,
                                    timeout=config.reqTimeout)
            else:  # mean POST. For user creation, autorization and submit post
                data = requests.post(request.url.replace(request.host_url, config.originURL),
                                     cookies=request.cookies,
                                     data=request.form.to_dict(),  # origin form data is ImmutableMultiDict
                                     timeout=config.reqTimeout)

            if "Content-Type" in data.headers.keys():
                if "text/html" in data.headers["Content-Type"]:
                    # Need to parse only html
                    addTM = AddTM()
                    resp = make_response(addTM.feed(data.text))
                else:
                    resp = make_response(data.content)
                # The only important header
                resp.headers["Content-Type"] = data.headers["Content-Type"]
            else:
                resp = make_response(data.content)

            if "/login" in request.url and request.method == "POST":
                # There is one 302 redirect, that places autorization cookie and which requests module follows
                # automatically
                resp.set_cookie("user", requests.utils.dict_from_cookiejar(data.history[0].cookies)["user"])

            if "/logout" in request.url:
                resp.delete_cookie("user")

            return resp

        except requests.Timeout:
            return make_response("Request timeout", 504)

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(host="localhost", port=5000)
