from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/about')
def about():
    return 'About me'


@app.route('/lists')
def get_lists():
    return 'All ToDo lists'


@app.route('/lists/<int:list_id>')
def get_list(list_id):
    return f'ToDo list {escape(list_id)}'


if __name__ == '__main__':
    app.run()
