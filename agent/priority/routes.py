from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service, Role, Users, Farmer, Agent, Situation, OrdersMaintenance, OrderStatus, Priority
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt

priority = Blueprint('priority',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')



# get priority 
@priority.route('/priority', methods=['POST', 'GET'])
@login_required
def get_priority():
    PriorityItems = db.session.query(Priority).all()
    return render_template('priority.html', PriorityItems = PriorityItems)


# insert new priority 
@priority.route('/priority/new', methods=['POST', 'GET'])
@login_required
def add_priority():
    if request.method == 'POST':
        NewPriority = Priority(PriorityName = request.form['PriorityName'])
        try :
            db.session.add(NewPriority)
            db.session.commit()
            flash('Yes !! Priority inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('priority.get_priority'))
        except Exception as err :
            flash('No !! ' + Sad + ' Priority did not insert successfully . Please check insertion ' , 'danger')
          
    return redirect(url_for('priority.get_priority'))


# edit priority
@priority.route('/priority/<int:IdPriority>/edit', methods=['POST', 'GET'])
@login_required
def edit_priority(IdPriority):
    if request.method == 'POST':
        EditPriority = db.session.query(Priority).filter_by(IdPriority = IdPriority).one()
        EditPriority.PriorityName = request.form['PriorityName']
        try :
            db.session.add(EditPriority)
            db.session.commit()
            flash('Yes !! Priority is edited successfully '+ Happy , 'success')
            return redirect(url_for('priority.get_priority'))
        except Exception as err :
            flash('No !! ' + Sad + ' Priority did not edit successfully . Please check insertion ' , 'danger')

    return redirect(url_for('priority.get_priority'))


# delete priority
@priority.route('/priority/<int:IdPriority>/delete', methods=['POST', 'GET'])
@login_required
def delete_priority(IdPriority):
    if request.method == 'GET':
        DeletePriority = db.session.query(Priority).filter_by(IdPriority = IdPriority).one()
        try :
            db.session.delete(DeletePriority)
            db.session.commit()
            flash('Yes !! Priority is deleted successfully '+ Happy , 'success')
            return redirect(url_for('priority.get_priority'))
        except Exception as err :
           flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
         
    return redirect(url_for('priority.get_priority'))
