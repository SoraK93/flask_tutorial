from flaskblog import app

if __name__ == "__main__":
	app.run(debug=True, host="LocalHost")

# with app.app_context():
	# db.create_all()
	# x = db.session.execute(db.select(User).where(User.id == 1)).scalar()
	# y = db.session.execute(db.select(Post).where(author_id==x.id)).scalar()
	# z = db.session.execute(db.select(Post).options(joinedload(Post.author))).scalar()
