from flask import Flask
from app.routes.view import bp

app = Flask(__name__)
app.register_blueprint(bp)
app.debug = True


if __name__ == '__main__':
    app.run()
