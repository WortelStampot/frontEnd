import os

from flask import Flask

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'schedlr.sqlite'),
		SQLALCHEMY_DATABASE_URI = 'sqlite:///sqlalchemy.db',
		)

	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	#ensure the instance referenced above folder exists
	try:
		os.mkdir(app.instance_path)
	except OSError: # when the folder already exists, there would be an error-
		pass # so we 'do nothing' as a success


	from . import db # initialize tutorial db
	db.init_app(app)
	
	from flask_sqlalchemy import SQLAlchemy # initialze sqlalchemy db
	from sqlalchemy.orm import DeclarativeBase

	class Base(DeclarativeBase):
		pass

	alchemyDB = SQLAlchemy(model_class=Base)
	alchemyDB.init_app(app)

	from sqlalchemy import Integer, String
	from sqlalchemy.orm import Mapped, mapped_column

	# set up the database model
	class User(alchemyDB.Model):
		id: Mapped[int] = mapped_column(Integer, primary_key=True)
		username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
		email: Mapped[str] = mapped_column(String)

	# create tables
	with app.app_context():
		alchemyDB.create_all()

	# query the data
	from flask import render_template, request, redirect, url_for
	@app.route('/users') #NOTE: seperate 'view' module? use Blueprint?
	def user_list():
		users = db.session.execute(
			db.select(User).order_by(User.username)
		)
		return render_template('user/list.html', users=users)

	@app.route('/user/create', methods=['POST', 'GET'])
	def user_create():
		if request.method == 'POST':
			user = User(
				username = request.form['username'],
				email = request.form['email'],
			)
			db.session.add(user)
			db.session.commit()
			return redirect(url_for('user_detail', id=user.id))
		
		return render_template('user/create.html')

	@app.route('/user/<int:id>')
	def user_detail(id):
		user = db.get_or_404(User, id)
		return render_template('user/detail.html', user=user)

	@app.route('/user/<int:id>/delete', methods=['POST', 'GET'])
	def user_delete(id):
		user = db.get_or_404(User, id)

		if request.method == 'POST':
			db.session.delete(user)
			db.session.commit()
			return redirect(url_for('user_list'))
		
		return render_template('user/delete.html', user=user)
		
	from . import auth
	app.register_blueprint(auth.bp)

	from . import blog
	app.register_blueprint(blog.bp)
	app.add_url_rule('/', endpoint='index')

	from . import table
	app.register_blueprint(table.blueprint)
	
	return app

	