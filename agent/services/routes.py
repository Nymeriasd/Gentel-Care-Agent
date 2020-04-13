from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service, Role, Users, Farmer, Agent,Situation, OrdersMaintenance, OrderStatus
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt

services = Blueprint('services',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')

# get all services
@services.route('/services', methods=['POST','GET'])
@login_required
def get_service():
    ServiceItems = db.session.query(Service).all()
    SituationItems = db.session.query(Situation).all()
    return render_template('services.html', ServiceItems = ServiceItems, SituationItems = SituationItems)

# add new services
@services.route('/services/new', methods=['POST','GET'])
@login_required
def add_service():
    if request.method == 'POST':
        NewService = Service(Name = request.form['ServiceName'], Price = request.form['Price'] , Enabled= request.form['Status'])
        try :
            db.session.add(NewService)
            db.session.commit()
            flash('Yes !! Service inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('services.get_service'))
        except Exception as err :
            flash('No !! ' + Sad + ' Service did not insert successfully . Please check insertion ' , 'danger')

    return redirect(url_for('services.get_service'))

# edit services
@services.route('/services/<int:IdService>/edit', methods=['POST','GET'])
@login_required
def edit_service(IdService):
    if request.method == 'POST':
        EditService = db.session.query(Service).filter_by(IdService = IdService).one()
        EditService.Name = request.form['ServiceName']
        EditService.Price = request.form['Price']
        EditService.Enabled = request.form['Status']
        try :
            db.session.add(EditService)
            db.session.commit()
            flash('Yes !! Service is edited successfully '+ Happy , 'success')
            return redirect(url_for('services.get_service'))
        except Exception as err :
            flash('No !! ' + Sad + ' Service did not edit successfully . Please check insertion ' , 'danger')
          
    return redirect(url_for('services.get_service'))

# delete services
@services.route('/services/<int:IdService>/delete', methods=['POST','GET'])
@login_required
def delete_service(IdService):
    if request.method == 'GET':
        DeleteService = db.session.query(Service).filter_by(IdService = IdService).one()
        try :
            db.session.delete(DeleteService)
            db.session.commit()
            flash('Yes !! Service is deleted successfully '+ Happy , 'success')
            return redirect(url_for('services.get_service'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
 
    return redirect(url_for('services.get_service'))
