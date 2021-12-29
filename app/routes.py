import os
import secrets
from PIL import Image
from flask import render_template, url_for, request, flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm
from app.models import User, Blogpost
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required


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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'Already Logged In!', 'success')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(f'Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/contact')
def contact():
    return render_template('contact.html')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)


#@app.route('/add')
#@login_required
#def add():
#    return render_template('add.html')

@app.route('/addpost', methods=['GET', 'POST'])
@login_required
def addpost():
    form = PostForm()
    if form.validate_on_submit():
        post = Blogpost(title=form.title.data, subtitle=form.subtitle.data,
                        author=current_user, content=form.content.data, date_posted=datetime.now())
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html', form=form)


#@app.route('/addpost', methods=['POST'])
#@login_required
#def addpost():
#    title = request.form['title']
#    subtitle = request.form['subtitle']
#    author = request.form['author']
#    content = request.form['content']
    #return '<h1>Title: {} Subtitle: {} Author: {} Content: {}</h1>'.format(title, subtitle, author, content)
#    post = Blogpost(title=title, subtitle=subtitle, author=author,
#                    content=content, date_posted=datetime.now())
#
#    db.session.add(post)
 #   db.session.commit()

 #   return redirect(url_for('index'))
