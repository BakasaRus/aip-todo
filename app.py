from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


todo_lists = [
    {
        'name': 'Литература',
        'items': [
            {'name': 'Крис Ричардсон, "Микросервисы. Паттерны разработки и рефакторинга"', 'is_done': True},
            {'name': 'Сэм Ньюмен, "От монолита к микросервисам"', 'is_done': False},
            {'name': 'Адам Беллемар, "Создание событийно-управляемых микросервисов"', 'is_done': False},
        ]
    },
    {
        'name': 'Академия',
        'items': [
            {'name': 'Блок занятий по технологиям разработки', 'is_done': True},
            {'name': 'Блок занятий по Flask', 'is_done': False},
            {'name': 'Блок занятий по БД и ORM', 'is_done': False},
        ]
    },
    {
        'name': 'Игры',
        'items': [
            {'name': 'The Legend of Zelda: Breath of the Wild', 'is_done': True},
            {'name': 'The Legend of Zelda: Skyward Sword', 'is_done': False},
            {'name': 'Super Mario Odyssey', 'is_done': True},
            {'name': 'Pokémon Legends: Arceus', 'is_done': False},
        ]
    },
]


@app.route('/')
def hello_world():
    return render_template('index.html', title="ToDon't", todo_lists=todo_lists)


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
