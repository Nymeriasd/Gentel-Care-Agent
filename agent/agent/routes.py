from flask_login import login_user, current_user, logout_user, login_required
from agent.models import Service, Role, Users, Farmer, Agent, Situation, OrdersMaintenance, OrderStatus, Time
from flask import abort, redirect, url_for, render_template, request, jsonify, flash, Markup, Blueprint
from agent import db, bcrypt

agent = Blueprint('agent',__name__)

Happy = Markup('<span>&#127881;</span>')
Sad = Markup('<span>&#128557;</span>')
Sassy = Markup('<span>&#128540;</span>')



# get all agent
@agent.route('/agent', methods=['POST', 'GET'])
@login_required
def get_agent():
    AgentItems = db.session.query(Agent).all()
    ServiceItems = db.session.query(Service).all()
    SituationItems = db.session.query(Situation).all()
    TimeItems = db.session.query(Time).all()
    return render_template('agent.html', AgentItems = AgentItems, ServiceItems = ServiceItems, SituationItems = SituationItems, TimeItems = TimeItems)

# add agent
@agent.route('/agent/new', methods=['POST', 'GET'])
@login_required
def add_agent():
    if request.method == 'POST' :
        NewAgent = Agent(FirstName = request.form['FirstName'], LastName = request.form['LastName'], Password = bcrypt.generate_password_hash(request.form['Password']).decode('utf-8'), PhoneNumber = request.form['PhoneNumber'], Address = request.form['Address'], IdService = request.form['Service'], Enabled = request.form['Status'], Time = request.form['Time'])
        try :
            db.session.add(NewAgent)
            db.session.commit()
            flash('Yes !! Agent inserted successfully. Great Job ' + current_user.FirstName + Happy , 'success')
            return redirect(url_for('agent.get_agent'))
        except Exception as err :
            flash('No !! ' + Sad + ' Agent did not insert successfully . Please check insertion ', 'danger')
        
    return redirect(url_for('agent.get_agent'))

# edit agent
@agent.route('/agent/<int:IdAgent>/edit', methods=['POST', 'GET'])
@login_required
def edit_agent(IdAgent):
    if request.method == 'POST':
        EditAgent = db.session.query(Agent).filter_by(IdAgent = IdAgent).one()
        EditAgent.FirstName = request.form['FirstName']
        EditAgent.LastName = request.form['LastName']
        EditAgent.Password = bcrypt.generate_password_hash(request.form['Password']).decode('utf-8')
        EditAgent.PhoneNumber = request.form['PhoneNumber']
        EditAgent.Address = request.form['Address']
        EditAgent.IdService = request.form['Service']
        EditAgent.Enabled = request.form['Status']
        EditAgent.Time = request.form['Time']
        try :
            db.session.add(EditAgent)
            db.session.commit()
            flash('Yes !! Agent is edited successfully '+ Happy , 'success')
            return redirect(url_for('agent.get_agent'))
        except Exception as err :
            flash('No !! ' + Sad + ' Agent did not edit successfully . Please check insertion ' , 'danger')
        
    return redirect(url_for('agent.get_agent'))

        

# delete agent
@agent.route('/agent/<int:IdAgent>/delete', methods=['POST', 'GET'])
@login_required
def delete_agent(IdAgent):
    if request.method == 'GET':
        DeleteAgent = db.session.query(Agent).filter_by(IdAgent = IdAgent).one()
        try :
            db.session.delete(DeleteAgent)
            db.session.commit()
            flash('Yes !! Agent is deleted successfully '+ Happy , 'success')
            return redirect(url_for('agent.get_agent'))
        except Exception as err :
            flash('NA NA NA you can delete me. Try again ' + Sassy  , 'danger')
          
    return redirect(url_for('agent.get_agent'))
