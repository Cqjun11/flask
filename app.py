from flask import Flask

app = Flask(__name__)


# @app.route('/')
# def hello_world():  # put application's code here
#     print(request.path)
#     print(request.full_path)
#     return request.args.__str__()


if __name__ == '__main__':
    app.run(debug=True)
