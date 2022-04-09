from flask import Flask, render_template, abort, request, redirect, url_for
from werkzeug import exceptions
from markupsafe import escape
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from forms import csrf, LoginForm, CreateTodoList, RegistrationForm, AddTodoItemForm
from models import db, bcrypt, User, TodoList, TodoItem
from os import environ

app = Flask(__name__)

uri = environ.get('DATABASE_URL')
if uri and uri.startswith('postgres://'):
    uri = uri.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = environ.get('APP_SECRET_KEY')

login_manager = LoginManager(app)
csrf.init_app(app)
db.app = app
db.init_app(app)
db.create_all()
bcrypt.init_app(app)


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


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


@app.route('/lists')
def get_lists():
    return 'All ToDo lists'


@app.route('/lists/create', methods=['GET', 'POST'])
@login_required
def create_list():
    create_todo_list_form = CreateTodoList()
    if create_todo_list_form.validate_on_submit():
        name = request.form.get('name')
        cover = request.form.get('cover')
        user_id = current_user.id
        new_todo = TodoList(name=name, cover=cover, user_id=user_id)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')
    return render_template('create_list.html', form=create_todo_list_form)


@app.route('/lists/<int:list_id>', methods=['GET', 'POST'])
@login_required
def get_list(list_id):
    todo_list = TodoList.query.get_or_404(list_id)
    if current_user.id != todo_list.user_id:
        abort(401)
    form = AddTodoItemForm()
    if form.validate_on_submit():
        name = request.form.get('name')
        new_item = TodoItem(name=name)
        todo_list.items.append(new_item)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('get_list', list_id=list_id))
    total_count = TodoItem.query.filter_by(list_id=list_id).count()
    done_count = TodoItem.query.filter_by(list_id=list_id, is_done=True).count()
    print(done_count, total_count)
    return render_template('list.html', todo_list=todo_list, done_count=done_count, total_count=total_count, form=form)


@app.route('/items/<int:item_id>/change-state', methods=['POST'])
def change_state(item_id):
    item = TodoItem.query.get_or_404(item_id)
    item.is_done = not item.is_done
    db.session.add(item)
    db.session.commit()
    print(item)
    return redirect(url_for('get_list', list_id=item.list_id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        email = request.form.get('email')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        user = User()
        user.email = email
        user.nickname = nickname
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', form=register_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect('/')
        else:
            return render_template('login.html', form=login_form)
    return render_template('login.html', form=login_form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.errorhandler(exceptions.NotFound)
def not_found(error):
    return render_template('404.html'), exceptions.NotFound.code


if __name__ == '__main__':
    app.run()
