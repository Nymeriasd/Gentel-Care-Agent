from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service,Role, Users, Farmer, Agent, Situation, OrdersMaintenance, OrderStatus
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt

users = Blueprint('users',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')

# get all users
@users.route('/users', methods=['POST','GET'])
@login_required
def get_users():
    User = db.session.query(Users).all()
    RoleItems = db.session.query(Role).all()
    SituationItems = db.session.query(Situation).all()
    return render_template("users.html", User = User , RoleItems = RoleItems, SituationItems = SituationItems)

# add new user
@users.route('/users/new', methods=['POST', 'GET'])
@login_required
def add_users():
    if request.method == 'POST' :
        NewUser = Users(IdRole = request.form['Role'], FirstName = request.form['FirstName'], LastName = request.form['LastName'], Email = request.form['Email'], PhoneNumber = request.form['PhoneNumber'], Address = request.form['Address'], Pasword = bcrypt.generate_password_hash(request.form['Pasword']).decode('utf-8'), Enabled = request.form['Status'])
        try :
            db.session.add(NewUser)
            db.session.commit()
            flash('Yes !! User inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('users.get_users'))
        except Exception as err :
            flash('No !! ' + Sad + ' User did not insert successfully . Please check insertion ', 'danger')
           
        return redirect(url_for('users.get_users'))

# edit User
@users.route('/users/<int:IdUser>/edit', methods=['POST','GET'])
@login_required
def edit_user(IdUser):
    if request.method == 'POST':
        EditUser = db.session.query(Users).filter_by(IdUser = IdUser).one()
        EditUser.IdRole = request.form['Role']
        EditUser.FirstName = request.form['FirstName']
        EditUser.LastName = request.form['LastName']
        EditUser.Email = Email = request.form['Email']
        EditUser.PhoneNumber = request.form['PhoneNumber']
        EditUser.Address =  request.form['Address']
        # EditUser.Pasword = bcrypt.generate_password_hash(request.form['Pasword']).decode('utf-8')
        EditUser.Enabled = request.form['Status']
        try :
            db.session.add(EditUser)
            db.session.commit()
            flash('Yes !! User is edited successfully '+ Happy , 'success')
            return redirect(url_for('users.get_users'))
        except Exception as err :
            flash('No !! ' + Sad + ' User did not edit successfully . Please check insertion ' , 'danger')

    return redirect(url_for('users.get_users'))

# delete user
@users.route('/users/<int:IdUser>/delete', methods=['POST', 'GET'])
@login_required
def delete_user(IdUser):
    if request.method == 'GET':
        DeleteUser  = db.session.query(Users).filter_by(IdUser = IdUser).one()
        try :
            db.session.delete(DeleteUser)
            db.session.commit()
            flash('Yes !! User is deleted successfully '+ Happy , 'success')
            return redirect(url_for('users.get_users'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')

    return redirect(url_for('users.get_users'))

# edit Passwod User
@users.route('/users_password/<int:IdUser>/edit', methods=['POST','GET'])
@login_required
def edit_password_user(IdUser):
    if request.method == 'POST':
        EditUser = db.session.query(Users).filter_by(IdUser = IdUser).one()
        EditUser.Pasword = bcrypt.generate_password_hash(request.form['Pasword']).decode('utf-8')
        try :
            db.session.add(EditUser)
            db.session.commit()
            flash('Yes !! Password is edited successfully '+ Happy , 'success')
            return redirect(url_for('users.get_users'))
        except Exception as err :
            flash('No !! ' + Sad + ' Password did not edit successfully . Please check insertion ' , 'danger')

    return redirect(url_for('users.get_users'))
