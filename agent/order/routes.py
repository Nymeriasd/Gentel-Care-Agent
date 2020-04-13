from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service, Role, Users, Farmer, Agent, Situation, OrdersMaintenance, OrderStatus, Priority, Time
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt
import random
import string
from datetime import datetime


orders = Blueprint('orders',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')

def random_string_generator(size=5,  chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# get orders
@orders.route('/order', methods=['POST', 'GET'])
@login_required
def get_order():
    OrdersItems = db.session.query(OrdersMaintenance).all()
    ServiceItems = db.session.query(Service).all()
    OrderStatusItems = db.session.query(OrderStatus).all()
    PriorityItems = db.session.query(Priority).all()
    TimeItems = db.session.query(Time).all()
    return render_template('orders.html', OrdersItems = OrdersItems, OrderStatusItems = OrderStatusItems, ServiceItems = ServiceItems, PriorityItems = PriorityItems, TimeItems = TimeItems)

# add new order
@orders.route('/order/new', methods=['POST', 'GET'])
@login_required
def add_order():
    if request.method == 'POST':
        GetService = db.session.query(Service).filter(Service.IdService == request.form['Services']).one()
        NewOrder = OrdersMaintenance(OrderNumber = "O"+random_string_generator(), FirstName = request.form['CustomerFirstName'], LastName = request.form['CustomerLastName'], PhoneNumber = request.form['CustomerPhone'], Address = request.form['CustomerAddress'], Email = request.form['CustomerEmail'], IdService = request.form['Services'], IdPriority = request.form['Priority'], IdOrderStatus = 1, Ordertime = request.form['Ordertime'], Price = GetService.Price, Comment = request.form['comment'], Time = request.form['Time'])
        try :
            db.session.add(NewOrder)
            db.session.commit()
    
            flash('Yes !! Order inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('orders.get_order'))
        except Exception as err :
            flash('No !! ' + Sad + ' Order did not insert successfully . Please check insertion ', 'danger')
 
    return redirect(url_for('orders.get_order'))

# edit order
@orders.route('/order/<int:IdOrder>/edit', methods=['POST', 'GET'])
@login_required
def edit_order(IdOrder):
    if request.method == 'POST':
        EditOrder = db.session.query(OrdersMaintenance).filter_by(IdOrder = IdOrder).one()
        EditOrder.FirstName = request.form['CustomerFirstName']
        EditOrder.FirstName  = request.form['CustomerLastName']
        EditOrder.PhoneNumber = request.form['CustomerPhone']
        EditOrder.Address = request.form['CustomerAddress']
        EditOrder.Email  = request.form['CustomerEmail']
        EditOrder.IdService  = request.form['Services']
        GetService = db.session.query(Service).filter(Service.IdService == EditOrder.IdService).one()
        EditOrder.IdPriority  = request.form['Priority']
        EditOrder.Ordertime  = request.form['Ordertime']
        EditOrder.Price  = GetService.Price
        EditOrder.Comment  = request.form['comment']
        EditOrder.Time  = request.form['Time']
        try :
            db.session.add(EditOrder)
            db.session.commit()
            flash('Yes !! Order is edited successfully '+ Happy , 'success')
            return redirect(url_for('orders.get_order'))
        except Exception as err :
            flash('No !! ' + Sad + ' Order did not edit successfully . Please check insertion ' , 'danger')
           
    return redirect(url_for('orders.get_order'))


# edit status order
@orders.route('/order/<int:IdOrder>/status', methods=['POST', 'GET'])
@login_required
def edit_status_order(IdOrder):
    if request.method == 'POST':
        EditOrder = db.session.query(OrdersMaintenance).filter_by(IdOrder = IdOrder).one()
        EditOrder.IdOrderStatus = request.form['OrderStatusName']
       
        try :
            db.session.add(EditOrder)
            db.session.commit()
            flash('Yes !! Order status is edited successfully '+ Happy , 'success')
            return redirect(url_for('orders.get_order'))
        except Exception as err :
            flash('No !! ' + Sad + ' Order status did not edit successfully . Please check insertion ' , 'danger')
         
    return redirect(url_for('orders.get_order'))


# delete Order
@orders.route('/order/<int:IdOrder>/delete', methods=['POST', 'GET'])
@login_required
def delete_order(IdOrder):
    if request.method == 'GET':
        DeleteOrder = db.session.query(OrdersMaintenance).filter_by(IdOrder = IdOrder).one()
        try :
            db.session.delete(DeleteOrder)
            db.session.commit()
            flash('Yes !! Order is deleted successfully '+ Happy , 'success')
            return redirect(url_for('orders.get_order'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
        
    return redirect(url_for('orders.get_order'))
