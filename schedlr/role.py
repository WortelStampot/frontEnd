from .model import alchemyDB, Role
from flask import Blueprint, render_template, request, redirect, url_for

blueprint = Blueprint('role', __name__)

@blueprint.route('/roles')
def listRoles():
    roles = alchemyDB.session.execute(
        alchemyDB.select(Role).order_by(Role.id)
    )
    return render_template('role/list.html', roles = roles)

@blueprint.route('/role/enter', methods=['POST', 'GET'])
def enterRole():
    if request.method == 'POST':
        role = Role(
            name= request.form['name'],
            callTime= request.form['callTime'],
            qualifiedStaff = request.form['qualifiedStaff'],
            perferredStaff = request.form['perferredStaff'],
        )
        alchemyDB.session.add(role)
        alchemyDB.session.commit()
        return redirect(url_for('role.listRoles'))
    
    return render_template('role/create.html')