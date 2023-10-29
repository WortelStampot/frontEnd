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
	except OSError:
		pass # do nothing?

	@app.route('/start')
	def a():
		return 'frontEnd'

	# -- sqlalchemy setup --
	from flask_sqlalchemy import SQLAlchemy
	from sqlalchemy.orm import DeclarativeBase
	
	class Base(DeclarativeBase):
		pass

	db = SQLAlchemy(model_class=Base)
	db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	from . import blog
	app.register_blueprint(blog.bp)
	app.add_url_rule('/', endpoint='index')

	from . import table
	app.register_blueprint(table.blueprint)
	
	return app

	