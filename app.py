from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


todo_list = {
    'name': 'Игры',
    'items': [
        {
            'name': 'The Legend of Zelda: Breath of the Wild',
            'is_done': True
        },
        {
            'name': 'The Legend of Zelda: Skyward Sword',
            'is_done': False
        },
        {
            'name': 'Super Mario Odyssey',
            'is_done': True
        },
        {
            'name': 'Pokémon Legends: Arceus',
            'is_done': False
        },
    ]
}


@app.route('/')
def hello_world():
    return render_template('index.html', title="ToDon't", todo_list=todo_list)


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
