from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.form import RegistrationForm, LoginForm
from flaskblog.models import User, Post

posts = {}


@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html", posts=posts)


@app.route("/about")
def about():
	return render_template("about.html", pagetitle="About")


@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		flash(f"Account created for {form.username.data}!", "success")
		return redirect(url_for('home'))
	return render_template("register.html", pagetitle="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == "admin@blog.com" and form.password.data == "password":
			flash("You have been logged in", "success")
			return redirect(url_for("home"))
		else:
			flash("Login Unsuccessful. Please check username/ password.", "danger")
	return render_template("login.html", pagetitle="Login", form=form)
