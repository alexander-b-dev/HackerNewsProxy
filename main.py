from flask import Flask
import config


def create_app():
    app = Flask(__name__, static_folder=r'WEB\static', template_folder=r'WEB\templates')
    app.config['DEBUG'] = config.debug
    app.config['SECRET_KEY'] = config.key

    @app.route('/')
    def index():
        pass

    return app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=5000)
