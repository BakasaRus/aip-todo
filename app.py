from flask import Flask, render_template, abort, request
from werkzeug import exceptions
from markupsafe import escape

app = Flask(__name__)


todo_lists = [
    {
        'id': 1,
        'name': 'Литература',
        'cover': 'images/books.jpg',
        'items': [
            {'name': 'Крис Ричардсон, "Микросервисы. Паттерны разработки и рефакторинга"', 'is_done': True},
            {'name': 'Сэм Ньюмен, "От монолита к микросервисам"', 'is_done': False},
            {'name': 'Адам Беллемар, "Создание событийно-управляемых микросервисов"', 'is_done': False},
        ]
    },
    {
        'id': 2,
        'name': 'Академия',
        'cover': 'images/aip.jpg',
        'items': [
            {'name': 'Блок занятий по технологиям разработки', 'is_done': True},
            {'name': 'Блок занятий по Flask', 'is_done': False},
            {'name': 'Блок занятий по БД и ORM', 'is_done': False},
        ]
    },
    {
        'id': 3,
        'name': 'Игры',
        'cover': 'images/games.jpg',
        'items': [
            {'name': 'The Legend of Zelda: Breath of the Wild', 'is_done': True},
            {'name': 'The Legend of Zelda: Skyward Sword', 'is_done': False},
            {'name': 'Super Mario Odyssey', 'is_done': True},
            {'name': 'Pokémon Legends: Arceus', 'is_done': False},
        ]
    },
]


@app.route('/')
def homepage():
    return render_template('index.html', title="ToDon't", todo_lists=todo_lists)


@app.route('/about')
def about():
    return 'About me'


@app.route('/search')
def search():
    text = escape(request.args.get('text', '').lower())
    selected_lists = [todo_list for todo_list in todo_lists if text in todo_list['name'].lower()]
    return render_template('index.html', todo_lists=selected_lists)


@app.route('/lists')
def get_lists():
    return 'All ToDo lists'


@app.route('/lists/<int:list_id>')
def get_list(list_id):
    if list_id > len(todo_lists):
        abort(exceptions.NotFound.code)
    return render_template('list.html', todo_list=todo_lists[list_id - 1])


@app.errorhandler(exceptions.NotFound)
def not_found(error):
    return render_template('404.html'), exceptions.NotFound.code


if __name__ == '__main__':
    app.run()
