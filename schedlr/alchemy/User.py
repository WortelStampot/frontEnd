from flask import current_app, request, url_for, redirect, render_template
from models import User, alchemyDB

@current_app.route('/users') #NOTE: seperate 'view' module? use Blueprint?
def user_list():
    users = alchemyDB.session.execute(
        alchemyDB.select(User).order_by(User.username)
    )
    return render_template('user/list.html', users=users)

@current_app.route('users/create', methods=['POST', 'GET'])
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

@current_app.route('/user/<int:id>')
def user_detail(id):
    user = alchemyDB.get_or_404(User, id)
    return render_template('user/detail.html', user=user)

@current_app.route('/user/<int:id>/delete', methods=['POST', 'GET'])
def user_delete(id):
    user = alchemyDB.get_or_404(User, id)

    if request.method == 'POST':
        alchemyDB.session.delete(user)
        alchemyDB.session.commit()
        return redirect(url_for('user_list'))
    
    return render_template('user/delete.html', user=user)
