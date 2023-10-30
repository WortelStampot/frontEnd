""" from flask import current_app, g,\
request, render_template, redirect, url_for #imports used for the sqlalchemy db

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
	pass

db = SQLAlchemy(model_class=Base)

current_app.config['SQLALCHEMY_DATABSE_URI'] = 'sqlite:///project.db'
db.init_app(current_app)

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

# set up the database model
class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String)

# create the tables
with current_app.app_context():
    db.create_all()

#query the data
@current_app.route('/users') #NOTE: seperate 'view' module? use Blueprint?
def user_list():
    users = db.session.execute(
        db.select(User).order_by(User.username)
    )
    return render_template('user/list.html', users=users)

@current_app.route('users/create', methods=['POST', 'GET'])
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

@current_app.route('/user/<int:id>')
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template('user/detail.html', user=user)

@current_app.route('/user/<int:id>/delete', methods=['POST', 'GET'])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == 'POST':
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('user_list'))
    
    return render_template('user/delete.html', user=user)
 """