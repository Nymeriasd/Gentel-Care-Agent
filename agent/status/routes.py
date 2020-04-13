from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service, Role, Users, Farmer, Agent, Situation, OrdersMaintenance, OrderStatus
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt

status = Blueprint('status',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')



# get status 
@status.route('/situation', methods=['POST', 'GET'])
@login_required
def get_situation():
    SituationItems = db.session.query(Situation).all()
    return render_template('status.html', SituationItems = SituationItems)


# insert new status 
@status.route('/situation/new', methods=['POST', 'GET'])
@login_required
def add_situation():
    if request.method == 'POST':
        NewSituation = Situation(Situation = request.form['SituationName'])
        try :
            db.session.add(NewSituation)
            db.session.commit()
            flash('Yes !! Status inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('status.get_situation'))
        except Exception as err :
            flash('No !! ' + Sad + ' Status did not insert successfully . Please check insertion ' , 'danger')
          
    return redirect(url_for('status.get_situation'))


# edit status
@status.route('/situation/<int:IdSituation>/edit', methods=['POST', 'GET'])
@login_required
def edit_situation(IdSituation):
    if request.method == 'POST':
        EditSituation = db.session.query(Situation).filter_by(IdSituation = IdSituation).one()
        EditSituation.Situation = request.form['SituationName']
        try :
            db.session.add(EditSituation)
            db.session.commit()
            flash('Yes !! Status is edited successfully '+ Happy , 'success')
            return redirect(url_for('status.get_situation'))
        except Exception as err :
            flash('No !! ' + Sad + ' Status did not edit successfully . Please check insertion ' , 'danger')

    return redirect(url_for('status.get_situation'))


# delete status
@status.route('/situation/<int:IdSituation>/delete', methods=['POST', 'GET'])
@login_required
def delete_situation(IdSituation):
    if request.method == 'GET':
        DeleteSituation = db.session.query(Situation).filter_by(IdSituation = IdSituation).one()
        try :
            db.session.delete(DeleteSituation)
            db.session.commit()
            flash('Yes !! Status is deleted successfully '+ Happy , 'success')
            return redirect(url_for('status.get_situation'))
        except Exception as err :
           flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
         
    return redirect(url_for('status.get_situation'))
