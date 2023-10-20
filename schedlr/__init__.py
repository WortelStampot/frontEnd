import os

from flask import Flask

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
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
	
	return app

	