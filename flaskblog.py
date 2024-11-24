import os
from dotenv import load_dotenv
from flask import Flask, render_template, url_for, flash, redirect
from form import RegistrationForm, LoginForm

app = Flask(__name__)
load_dotenv()

app.config["SECRET_KEY"] = "3b1897ae82f207e25bab6779c4fcc234"
# app.config["SECRET_KEY"] = os.environ("FLASK_KEY")


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


if __name__ == "__main__":
	app.run(debug=True, host="LocalHost")

