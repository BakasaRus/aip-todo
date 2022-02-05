from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/about')
def about():
    return 'About me'


if __name__ == '__main__':
    app.run()
