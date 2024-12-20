import os, secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.form import (RegistrationForm, LoginForm, UpdateAccountForm,
                            PostForm, RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post
from flask_login import login_user, login_required, logout_user, current_user
from PIL import Image


@app.route("/")
@app.route("/home")
def home():
	page = request.args.get("page", 1, type=int)
	posts = db.paginate(db.select(Post).order_by(Post.date_posted.desc()), page=page, per_page=5)
	return render_template("home.html", posts=posts)


@app.route("/about")
def about():
	return render_template("about.html", pagetitle="About")


@app.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		new_user = User(
			username=form.username.data,
			email=form.email.data,
			password=hashed_password
		)
		db.session.add(new_user)
		db.session.commit()
		flash("Your account has been created! You are able to login", "success")
		return redirect(url_for('login'))
	return render_template("register.html", pagetitle="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
	next_page = request.args.get("next")
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = LoginForm()
	if form.validate_on_submit():
		user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar_one_or_none()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(next_page) if next_page else redirect(url_for("home"))
		else:
			flash("Login Unsuccessful. Please check Email and Password.", "danger")
	return render_template("login.html", pagetitle="Login", form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))


def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn


@app.route("/account", methods=["GET", "POST"])
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
		flash("Your account has been updated", "success")
		return redirect(url_for("account"))
	elif request.method == "GET":
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename="profile_pics/" + current_user.image_file)
	return render_template("account.html", pagetitle="Account", image_file=image_file, form=form)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(
			title=form.title.data,
			content=form.content.data,
			author=current_user
		)
		db.session.add(post)
		db.session.commit()
		flash("Your post has been created", "success")
		return redirect(url_for("home"))
	return render_template("create_post.html", pagetitle="New Post", form=form, legend="Update Post")


@app.route("/post/<int:post_id>")
def post(post_id):
	single_post = db.get_or_404(Post, post_id)
	return render_template("post.html", pagetitle=single_post.title, post=single_post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update(post_id):
	single_post = db.get_or_404(Post, post_id)
	if single_post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		single_post.title = form.title.data
		single_post.content = form.content.data
		db.session.commit()
		flash("Your post has been updated.", "success")
		return redirect(url_for("post", post_id=single_post.id))
	elif request.method == "GET":
		form.title.data = single_post.title
		form.content.data = single_post.content
	return render_template("create_post.html", pagetitle="Update Post", form=form, legend="Update Post")


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete(post_id):
	single_post = db.get_or_404(Post, post_id)
	if single_post.author != current_user:
		abort(403)
	db.session.delete(single_post)
	db.session.commit()
	flash("Your post has been deleted.", "success")
	return redirect(url_for("home"))


@app.route("/user/<string:name>/")
def user_posts(name):
	page = request.args.get('page', 1, type=int)
	user = db.session.execute(db.select(User).filter_by(username=name)).scalars().first()
	posts = db.paginate(
		db.select(Post).
		filter_by(author=user).
		order_by(Post.date_posted.desc()),
		page=page,
		per_page=5
	)
	return render_template("user_post.html", posts=posts, user=user)


def send_reset_email(user):
	pass


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = db.session.execute(db.select(User).filter_by(email=form.email.data)).first()
		send_reset_email(user)
		flash("An email has been sent with instructions to reset your password.", "info")
		return redirect(url_for("login"))
	return render_template("reset_request.html", pagetitle="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	user = User.verify_reset_token(token)
	if user is None:
		flash("That is a invalid or expired token.", "warning")
		return redirect(url_for("reset_request"))
	form = ResetPasswordForm()
	return render_template("reset_token.html", title="Reset Password", form=form)
