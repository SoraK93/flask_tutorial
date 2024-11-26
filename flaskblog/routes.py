from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt, login_manager
from flaskblog.form import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, login_required, logout_user, current_user

posts = [
	{
		"author": "Sora",
		"title": "Blog Post 1",
		"content": "First post content",
		"date_posted": "April 20, 2018",
	},
	{
		"author": "Sham",
		"title": "Blog Post 2",
		"content": "Second post content",
		"date_posted": "April 21, 2018",
	}
]


@app.route("/")
@app.route("/home")
def home():
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
	print(f"1.{next_page}")
	if current_user.is_authenticated:
		return redirect(url_for("home"))
	form = LoginForm()
	print(f"2.{next_page}")
	if form.validate_on_submit():
		user = db.session.execute(db.select(User).filter_by(email=form.email.data)).scalar_one_or_none()
		print(f"3.{next_page}")
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			print(f"4.{next_page}")
			return redirect(next_page) if next_page else redirect(url_for("home"))
		else:
			flash("Login Unsuccessful. Please check Email and Password.", "danger")
	return render_template("login.html", pagetitle="Login", form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))


@app.route("/account")
@login_required
def account():
	return render_template("account.html", title="Account")


