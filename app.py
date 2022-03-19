from flask import Flask, render_template, abort, request, redirect
from werkzeug import exceptions
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'rtdgykjio;hugly&&fuvhjb,uoi89t76cfjh!g8p!u9w7'
db = SQLAlchemy(app)
csrf = CSRFProtect(app)


class TodoList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    cover = db.Column(db.Text)
    items = db.relationship('TodoItem', backref='list', lazy=True)

    def __repr__(self):
        return f'<TodoList {self.name}>'


class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    is_done = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todo_list.id'), nullable=False)


class CreateTodoList(FlaskForm):
    name = StringField('Название')
    cover = StringField('Ссылка на обложку')


@app.route('/')
def homepage():
    todo_lists = TodoList.query.all()
    return render_template('index.html', title="ToDon't", todo_lists=todo_lists)


@app.route('/about')
def about():
    return 'About me'


@app.route('/search')
def search():
    text = escape(request.args.get('text', ''))
    selected_lists = TodoList.query.filter(TodoList.name.like(f'%{text}%')).all()
    return render_template('index.html', todo_lists=selected_lists)


@app.route('/lists', methods=['GET', 'POST'])
def get_lists():
    create_todo_list_form = CreateTodoList()
    if create_todo_list_form.validate_on_submit():
        name = request.form.get('name')
        cover = request.form.get('cover')
        new_todo = TodoList(name=name, cover=cover)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')
    else:
        return 'All ToDo lists'


@app.route('/lists/create')
def create_list():
    create_todo_list_form = CreateTodoList()
    return render_template('create_list.html', form=create_todo_list_form)


@app.route('/lists/<int:list_id>')
def get_list(list_id):
    todo_list = TodoList.query.get_or_404(list_id)
    return render_template('list.html', todo_list=todo_list)


@app.errorhandler(exceptions.NotFound)
def not_found(error):
    return render_template('404.html'), exceptions.NotFound.code


if __name__ == '__main__':
    app.run()
