import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session, abort
from app import app, db, bcrypt
from app.form import Register, Login, Segment, UpdateAccountForm, AdminLogin
from app.models import User, Data
from flask_login import login_user, current_user, logout_user, login_required
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

@app.route('/')
@app.route('/first')
def first():
    return render_template('first.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = Register()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, phone=form.phone.data, password=hashed_password, code=form.passcode.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)


admin = Admin(app)
admin.add_view(SecureModelView(User,db.session))
admin.add_view(SecureModelView(Data,db.session))


@app.route("/admin_logout")
def admin_logout():
    session.clear()
    return redirect("/")


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    form = AdminLogin()
    if form.validate_on_submit():
        if form.username.data == "admin" and form.password.data == "mimbulus1902":
            session['logged_in'] = True
            return redirect("/admin")
        else:
            flash('Invalid', 'danger')
    return render_template("admin_login.html", form=form)


@app.route("/home")
@login_required
def home():
    return redirect(url_for('user_data', email=current_user.email))


@app.route("/user_data/<string:email>")
@login_required
def user_data(email):
    user = User.query.filter_by(email=email).first_or_404()
    posts = Data.query.filter_by(author=user)
    return render_template('home.html', posts=posts, user=user)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
   random_hex = secrets.token_hex(8)
   _, f_ext = os.path.splitext(form_picture.filename)
   picture_fn = random_hex + f_ext
   picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

   output_size = (125, 125)
   i = Image.open(form_picture)
   i.thumbnail(output_size)
   i.save(picture_path)

   return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/segment/new", methods=['GET', 'POST'])
@login_required
def new_segment():
    form = Segment()
    if form.validate_on_submit():
        post = Data(segment_name=form.segment_name.data, username=form.username.data, password=form.password.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your data has been saved!', 'success')
        return redirect(url_for('home'))
    return render_template('new_segment.html', title='New Segment', form=form, legend='New Segment')


@app.route("/segment/<int:user_id>/<int:post_id>", methods=['GET', 'POST'])
def segment(post_id, user_id):
    post = Data.query.get_or_404(post_id)
    data = User.query.get_or_404(user_id)
    return render_template('segment.html', title=post.segment_name, post=post, data=data)


@app.route("/segment/<int:user_id>/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_segment(post_id, user_id):
    post = Data.query.get(post_id)
    data = User.query.get(user_id)
    if post.author != current_user:
        abort(403)
    form = Segment()
    if form.validate_on_submit():
        post.segment_name = form.segment_name.data
        post.username = form.username.data
        post.password = form.password.data
        db.session.commit()
        flash('Your Segment has been updated!', 'success')
        return redirect(url_for('segment', post_id=post.id, user_id=data.id))
    elif request.method == 'GET':
        form.segment_name.data = post.segment_name
        form.username.data = post.username
        form.password.data = post.password
    return render_template('new_segment.html', title='Update Segment', form=form, legend='Update Segment')


@app.route("/segment/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_segment(post_id):
    post = Data.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Segment has been deleted!', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

