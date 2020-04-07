from flask import Flask, render_template, request, redirect, make_response, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.login_form import LoginForm
from data.register_form import RegisterForm
from data.news_form import NewsForm

import datetime

from data.db_session import create_session, global_init
from data.news import News
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfjdkfjdkfjdkfdj'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_session = create_session()
    return db_session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_session = create_session()
        user = db_session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message="Неправильный логин и пароль", form=form, title="Авторизация")
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/testing')
def testing():
    return render_template("test.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    db_session = create_session()

    if form.validate_on_submit():
        user = User()
        user.name = form['name'].data
        user.surname = form['surname'].data
        user.age = form['age'].data
        user.position = form['position'].data
        user.speciality = form['speciality'].data
        user.address = form['address'].data
        user.email = form['login_email'].data
        user.set_password(form['password'].data)
        user.modified_date = datetime.datetime.now()
        db_session.add(user)
        db_session.commit()
        return redirect('/')
    else:
        return render_template('register.html', form=form, title="Register Form")


@app.route('/')
def news_journal():
    db_session = create_session()

    if current_user.is_authenticated:
        news = db_session.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_session.query(News).filter(News.is_private != True)

    return render_template('news_journal.html', title='Новости', news=news)


@app.route('/add_news', methods=['GET', 'POST'])
@login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_session = create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_session.merge(current_user)

        db_session.commit()
        return redirect('/')
    return render_template('add_news.html', title='Добавление новости', form=form)


@app.route('/edit_news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = NewsForm()
    if request.method == 'GET':
        db_session = create_session()
        news = db_session.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_session = create_session()
        news = db_session.query(News).filter(News.id == id, News.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_session.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_news.html', title='Редактирование новости', form=form)


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_session = create_session()
    news = db_session.query(News).filter(News.id == id,
                                      News.user == current_user).first()
    if news:
        db_session.delete(news)
        db_session.commit()
    else:
        abort(404)
    return redirect('/')


def main():
    global_init('db/blogs.sqlite')

    app.run(host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
