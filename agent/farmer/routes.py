from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service, Role, Users, Farmer, Agent, Situation, OrdersMaintenance, OrderStatus
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt

farmer = Blueprint('farmer',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')


# get all farmers
@farmer.route('/customer', methods=['POST','GET'])
@login_required
def get_farmer():
    FarmerItems = db.session.query(Farmer).all()
    return render_template('farmers.html', FarmerItems = FarmerItems)

# add new farmer
@farmer.route('/customer/new', methods=['POST','GET'])
@login_required
def add_farmer():
    if request.method == 'POST':
        NewFarmer = Farmer(FirstName = request.form['FirstName'], LastName = request.form['LastName'], PhoneNumber = request.form['PhoneNumber'], Address = request.form['Address'], IdCrop = request.form['Crop'], Harvestime = request.form['Harvestime'])
        try :
            db.session.add(NewFarmer)
            db.session.commit()
            flash('Yes !! Customer inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('farmer.get_farmer'))
        except Exception as err :
            flash('No !! ' + Sad + ' Customer did not insert successfully . Please check insertion ', 'danger')
          
    return redirect(url_for('farmer.get_farmer'))


# edit farmer
@farmer.route('/customer/<int:Idfarmer>/edit', methods=['POST','GET'])
@login_required
def edit_farmer(Idfarmer):
    if request.method == 'POST' :
        EditFarmer = db.session.query(Farmer).filter_by(Idfarmer = Idfarmer).one()
        EditFarmer.FirstName = request.form['FirstName']
        EditFarmer.LastName = request.form['LastName']
        EditFarmer.PhoneNumber = request.form['PhoneNumber']
        EditFarmer.Address = request.form['Address']
        EditFarmer.IdCrop = request.form['Crop']
        EditFarmer.Harvestime = request.form['Harvestime']
        try :
            db.session.add(EditFarmer)
            db.session.commit()
            flash('Yes !! Customer is edited successfully '+ Happy , 'success')
            return redirect(url_for('farmer.get_farmer'))
        except Exception as err :
            flash('No !! ' + Sad + ' Customer did not edit successfully . Please check insertion ' , 'danger')
          
    return redirect(url_for('farmer.get_farmer'))


# delete farmer
@farmer.route('/customer/<int:Idfarmer>/delete', methods=['POST', 'GET'])
@login_required
def delete_farmer(Idfarmer):
    if request.method == 'GET' :
        DeleteFarmer = db.session.query(Farmer).filter_by(Idfarmer = Idfarmer).one()
        try :
            db.session.delete(DeleteFarmer)
            db.session.commit()
            flash('Yes !! Customer is deleted successfully '+ Happy , 'success')
            return redirect(url_for('farmer.get_farmer'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
           
    return redirect(url_for('farmer.get_farmer'))
