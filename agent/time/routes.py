from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service,Role, Users, Farmer, Agent,Situation, OrdersMaintenance, OrderStatus, Time
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt

time = Blueprint('time',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')



# get all roles
@time.route('/time', methods=['POST', 'GET'])
@login_required
def get_time():
    TimeItems = db.session.query(Time).all()
    return render_template('time.html', TimeItems = TimeItems)


# add new role
@time.route('/time/new', methods=['POST', 'GET'])
@login_required
def add_time():
    if request.method == 'POST':
        NewTime = Time(TimeDec = request.form['Time'])
        try :
            db.session.add(NewTime)
            db.session.commit()
            flash('Yes !! Time inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('time.get_time'))
        except Exception as err :
            flash('No !! ' + Sad + ' Time did not insert successfully . Please check insertion ', 'danger')

    return redirect(url_for('time.get_time'))

# edit role
@time.route('/time/<int:IdTime>/edit', methods=['POST', 'GET'])
@login_required
def edit_time(IdTime):
    if request.method == 'POST':
        EditTime = db.session.query(Time).filter_by(IdTime = IdTime).one()
        EditTime.TimeDec = request.form['Time']
        try :
            db.session.add(EditTime)
            db.session.commit()
            flash('Yes !! Time is edited successfully '+ Happy , 'success')
            return redirect(url_for('time.get_time'))
        except Exception as err :
            flash('No !! ' + Sad + ' Time did not edit successfully . Please check insertion ' , 'danger')

    return redirect(url_for('time.get_time'))

# delete role
@time.route('/time/<int:IdTime>/delete', methods=['POST', 'GET'])
@login_required
def delete_time(IdTime):
    if request.method == 'GET':
        DeleteTime = db.session.query(Role).filter_by(IdTime = IdTime).one()
        try :
            db.session.delete(DeleteTime)
            db.session.commit()
            flash('Yes !! Time is deleted successfully '+ Happy , 'success')
            return redirect(url_for('time.get_time'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
          
    return redirect(url_for('time.get_time'))
