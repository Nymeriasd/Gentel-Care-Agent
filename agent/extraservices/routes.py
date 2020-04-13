from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service, Role, Users, Farmer, Agent,Situation, OrdersMaintenance, OrderStatus, ExtraService
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt

extraservices = Blueprint('extraservices',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')

# get all extraservices
@extraservices.route('/extraservices', methods=['POST','GET'])
@login_required
def get_extraservices():
    ExtraServiceItems = db.session.query(ExtraService).all()
    SituationItems = db.session.query(Situation).all()
    return render_template('extraservices.html', ExtraServiceItems = ExtraServiceItems, SituationItems = SituationItems)

# add new services
@extraservices.route('/extraservices/new', methods=['POST','GET'])
@login_required
def add_extraservices():
    if request.method == 'POST':
        NewExtraService = ExtraService(Name = request.form['ServiceName'], Price = request.form['Price'] , Enabled= request.form['Status'])
        try :
            db.session.add(NewExtraService)
            db.session.commit()
            flash('Yes !! Extra Service inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('extraservices.get_extraservices'))
        except Exception as err :
            flash('No !! ' + Sad + ' Extra Service did not insert successfully . Please check insertion ' , 'danger')

    return redirect(url_for('extraservices.get_extraservices'))

# edit services
@extraservices.route('/extraservices/<int:IdService>/edit', methods=['POST','GET'])
@login_required
def edit_extraservices(IdService):
    if request.method == 'POST':
        EditExtraService = db.session.query(ExtraService).filter_by(IdService = IdService).one()
        EditExtraService.Name = request.form['ServiceName']
        EditExtraService.Price = request.form['Price']
        EditExtraService.Enabled = request.form['Status']
        try :
            db.session.add(EditExtraService)
            db.session.commit()
            flash('Yes !! Extra Service is edited successfully '+ Happy , 'success')
            return redirect(url_for('extraservices.get_extraservices'))
        except Exception as err :
            flash('No !! ' + Sad + ' Extra Service did not edit successfully . Please check insertion ' , 'danger')
          
    return redirect(url_for('extraservices.get_extraservices'))

# delete services
@extraservices.route('/extraservices/<int:IdService>/delete', methods=['POST','GET'])
@login_required
def delete_extraservices(IdService):
    if request.method == 'GET':
        DeleteExtraService = db.session.query(ExtraService).filter_by(IdService = IdService).one()
        try :
            db.session.delete(DeleteExtraService)
            db.session.commit()
            flash('Yes !! Extra Service is deleted successfully '+ Happy , 'success')
            return redirect(url_for('extraservices.get_extraservices'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
 
    return redirect(url_for('extraservices.get_extraservices'))
