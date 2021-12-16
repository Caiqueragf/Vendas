from flask import render_template, url_for, request, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Blogpost
from datetime import datetime

about_text = 'Testando'

@app.route('/')
@app.route('/index')
def index():
    posts = Blogpost.query.all()
    return render_template('index.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    date_posted = post.date_posted.strftime('%B %d, %Y')
    return render_template('post.html', post=post, date_posted=date_posted)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/account', methods=['GET', 'POST'])
def account():
    return render_template('account.html', text=about_text)


@app.route('/add')
def add():
    return render_template('add.html')


@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    #return '<h1>Title: {} Subtitle: {} Author: {} Content: {}</h1>'.format(title, subtitle, author, content)
    post = Blogpost(title=title, subtitle=subtitle, author=author,
                    content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))
