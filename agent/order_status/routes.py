from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service, Role, Users, Farmer, Agent, Situation, OrdersMaintenance, OrderStatus
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt

order_status = Blueprint('order_status',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')


# get  order status 
@order_status.route('/order_status', methods=['POST', 'GET'])
@login_required
def get_order_status():
    OrderStatusItems = db.session.query(OrderStatus).all()
    return render_template('order_status.html', OrderStatusItems = OrderStatusItems)


# insert new order status 
@order_status.route('/order_status/new', methods=['POST', 'GET'])
@login_required
def add_order_status():
    if request.method == 'POST':
        NewOrderStatus = OrderStatus(OrderStatus = request.form['OrderStatusName'])
        try :
            db.session.add(NewOrderStatus)
            db.session.commit()
            flash('Yes !! Order status inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('order_status.get_order_status'))
        except Exception as err :
            flash('No !! ' + Sad + ' Order status did not insert successfully . Please check insertion ', 'danger')
         
    return redirect(url_for('order_status.get_order_status'))


# edit order status
@order_status.route('/order_status/<int:IdOrderStatus>/edit', methods=['POST', 'GET'])
@login_required
def edit_order_status(IdOrderStatus):
    if request.method == 'POST':
        EditOrderStatus = db.session.query(OrderStatus).filter_by(IdOrderStatus = IdOrderStatus).one()
        EditOrderStatus.OrderStatus = request.form['OrderStatusName']
        try :
            db.session.add(EditOrderStatus)
            db.session.commit()
            flash('Yes !! Order status is edited successfully '+ Happy , 'success')
            return redirect(url_for('order_status.get_order_status'))
        except Exception as err :
            flash('No !! ' + Sad + ' Order status did not edit successfully . Please check insertion ' , 'danger')
           
    return redirect(url_for('order_status.get_order_status'))


# delete order status
@order_status.route('/order_status/<int:IdOrderStatus>/delete', methods=['POST', 'GET'])
@login_required
def delete_order_status(IdOrderStatus):
    if request.method == 'GET':
        DeleteOrderStatus = db.session.query(OrderStatus).filter_by(IdOrderStatus = IdOrderStatus).one()
        try :
            db.session.delete(DeleteOrderStatus)
            db.session.commit()
            flash('Yes !! Order status is deleted successfully '+ Happy , 'success')
            return redirect(url_for('order_status.get_order_status'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
           
    return redirect(url_for('order_status.get_order_status'))
