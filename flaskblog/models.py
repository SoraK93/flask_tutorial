from datetime import datetime
from flaskblog import db, login_manager
from sqlalchemy import String, ForeignKey, Integer, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return db.get_or_404(User, user_id)


class User(db.Model, UserMixin):
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
