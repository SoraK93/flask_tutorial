import os
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Integer, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from form import RegistrationForm, LoginForm

load_dotenv()


class Base(DeclarativeBase):
	pass


db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db.init_app(app)


class User(db.Model):
	__tablename__ = "user"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
	email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
	image_file: Mapped[str] = mapped_column(String(20), nullable=False, default='default.jpg')
	password: Mapped[str] = mapped_column(String(60), nullable=False)
	# This will link the user to their posts
	posts = relationship('Post', back_populates="author")

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	__tablename__ = "post"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	title: Mapped[str] = mapped_column(String(100), nullable=False)
	date_posted: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
	content: Mapped[str] = mapped_column(Text, nullable=False)
	author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
	# This will link the post to the user that wrote it.
	author = relationship("User", back_populates="posts")

	def __repr__(self):
		return f"Post('{self.title}','{self.date_posted}')"


# with app.app_context():
	# db.create_all()

	# x = db.session.execute(db.select(User).where(User.id == 1)).scalar()

	# y = db.session.execute(db.select(Post).where(author_id==x.id)).scalar()

	# z = db.session.execute(db.select(Post).options(joinedload(Post.author))).scalar()


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

