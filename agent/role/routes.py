from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service,Role, Users, Farmer, Agent,Situation, OrdersMaintenance, OrderStatus
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt

role = Blueprint('role',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')



# get all roles
@role.route('/role', methods=['POST', 'GET'])
@login_required
def get_role():
    RoleItems = db.session.query(Role).all()
    return render_template('role.html', RoleItems = RoleItems)


# add new role
@role.route('/role/new', methods=['POST', 'GET'])
@login_required
def add_role():
    if request.method == 'POST':
        NewRole = Role(Role = request.form['RoleName'])
        try :
            db.session.add(NewRole)
            db.session.commit()
            flash('Yes !! Role inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('role.get_role'))
        except Exception as err :
            flash('No !! ' + Sad + ' Role did not insert successfully . Please check insertion ', 'danger')

    return redirect(url_for('role.get_role'))

# edit role
@role.route('/role/<int:IdRole>/edit', methods=['POST', 'GET'])
@login_required
def edit_role(IdRole):
    if request.method == 'POST':
        EditRole = db.session.query(Role).filter_by(IdRole = IdRole).one()
        EditRole.Role = request.form['RoleName']
        try :
            db.session.add(EditRole)
            db.session.commit()
            flash('Yes !! Role is edited successfully '+ Happy , 'success')
            return redirect(url_for('role.get_role'))
        except Exception as err :
            flash('No !! ' + Sad + ' Role did not edit successfully . Please check insertion ' , 'danger')

    return redirect(url_for('role.get_role'))

# delete role
@role.route('/role/<int:IdRole>/delete', methods=['POST', 'GET'])
@login_required
def delete_role(IdRole):
    if request.method == 'GET':
        DeleteRole = db.session.query(Role).filter_by(IdRole = IdRole).one()
        try :
            db.session.delete(DeleteRole)
            db.session.commit()
            flash('Yes !! Role is deleted successfully '+ Happy , 'success')
            return redirect(url_for('role.get_role'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
          
    return redirect(url_for('role.get_role'))
