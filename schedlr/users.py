from .model import alchemyDB, User
from flask import Blueprint, render_template, request, redirect, url_for

blueprint = Blueprint('users', __name__)

@blueprint.route('/users') #NOTE: seperate 'view' module? use Blueprint?
def user_list():
    users = alchemyDB.session.execute(
        alchemyDB.select(User).order_by(User.username)
    )
    return render_template('user/list.html', users=users)

@blueprint.route('/user/create', methods=['POST', 'GET'])
def user_create():
    if request.method == 'POST':
        user = User(
            username = request.form['username'],
            email = request.form['email'],
        )
        alchemyDB.session.add(user)
        alchemyDB.session.commit()
        return redirect(url_for('user_detail', id=user.id))
    
    return render_template('user/create.html')

@blueprint.route('/user/<int:id>')
def user_detail(id):
    user = alchemyDB.get_or_404(User, id)
    return render_template('user/detail.html', user=user)

@blueprint.route('/user/<int:id>/delete', methods=['POST', 'GET'])
def user_delete(id):
    user = alchemyDB.get_or_404(User, id)

    if request.method == 'POST':
        alchemyDB.session.delete(user)
        alchemyDB.session.commit()
        return redirect(url_for('user_list'))
    
    return render_template('user/delete.html', user=user)