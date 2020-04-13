from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service, Role, Users, Farmer, Agent, Situation, OrdersMaintenance, OrderStatus
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt

condition = Blueprint('condition',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')

# get  condition
@condition.route('/condition', methods=['POST', 'GET'])
@login_required
def get_condition():
    conditionItems = db.session.query(Conditions).all()
    return render_template('condition.html', conditionItems = conditionItems)


# insert new condition
@condition.route('/condition/new', methods=['POST', 'GET'])
@login_required
def add_condition():
    if request.method == 'POST':
        NewCondition = Conditions(ConditionName = request.form['ConditionName'])
        try :
            db.session.add(NewCondition)
            db.session.commit()
            flash('Yes !! Condition inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('condition.get_condition'))
        except Exception as err :
            flash('No !! ' + Sad + ' Condition did not insert successfully . Please check insertion ', 'danger')
         
    return redirect(url_for('condition.get_condition'))


# edit Condition
@condition.route('/condition/<int:IdCondition>/edit', methods=['POST', 'GET'])
@login_required
def edit_condition(IdCondition):
    if request.method == 'POST':
        EditCondition = db.session.query(Conditions).filter_by(IdCondition = IdCondition).one()
        EditCondition.ConditionName = request.form['ConditionName']
        try :
            db.session.add(EditCondition)
            db.session.commit()
            flash('Yes !! Condition is edited successfully '+ Happy , 'success')
            return redirect(url_for('condition.get_condition'))
        except Exception as err :
            flash('No !! ' + Sad + ' Condition did not edit successfully . Please check insertion ' , 'danger')
           
    return redirect(url_for('condition.get_condition'))


# delete order status
@condition.route('/condition/<int:IdCondition>/delete', methods=['POST', 'GET'])
@login_required
def delete_condition(IdCondition):
    if request.method == 'GET':
        DeleteCondition = db.session.query(Conditions).filter_by(IdCondition = IdCondition).one()
        try :
            db.session.delete(DeleteCondition)
            db.session.commit()
            flash('Yes !! Condition is deleted successfully '+ Happy , 'success')
            return redirect(url_for('condition.get_condition'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
           
    return redirect(url_for('condition.get_condition'))
