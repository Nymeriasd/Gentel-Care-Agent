from agent import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(IdAgent):
    return Agent.query.get(int(IdAgent))



class Service(db.Model):
    IdService = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(250), nullable=False)
    Price = db.Column(db.String(250), nullable=False)
    Enabled = db.Column(db.Integer, db.ForeignKey('situation.IdSituation'))
    CreatedAt = db.Column(db.DateTime, nullable=False) 
    situation = db.relationship('Situation', backref='Service')

    def __repr__(self) :
        return f"Service('{self.IdService}','{self.Name},'{self.Price}','{self.Enabled}','{self.CreatedAt}')"


class ExtraService(db.Model):
    IdService = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(250), nullable=False)
    Price = db.Column(db.String(250), nullable=False)
    Enabled = db.Column(db.Integer, db.ForeignKey('situation.IdSituation'))
    CreatedAt = db.Column(db.DateTime, nullable=False) 
    situation = db.relationship('Situation', backref='ExtraService')

    def __repr__(self) :
        return f"ExtraService('{self.IdService}','{self.Name},'{self.Price}','{self.Enabled}','{self.CreatedAt}')"



class Role(db.Model):
    IdRole = db.Column(db.Integer, primary_key=True)
    Role = db.Column(db.String(250), nullable=False)
    CreatedAt = db.Column(db.DateTime, nullable=False) 

    def __repr__(self) :
        return f"Role('{self.IdRole}','{self.Role},'{self.CreatedAt}')"

class Users(db.Model, UserMixin):
    IdUser = db.Column(db.Integer, primary_key=True)
    IdRole = db.Column(db.Integer, db.ForeignKey('role.IdRole'))
    FirstName = db.Column(db.String(250), nullable=True)
    LastName = db.Column(db.String(250), nullable=True)
    Email = db.Column(db.String(250), nullable=True)
    PhoneNumber = db.Column(db.String(250), nullable=True)
    Address = db.Column(db.String(250), nullable=True)
    Pasword = db.Column(db.String(250), nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False) 
    Enabled = db.Column(db.Integer, db.ForeignKey('situation.IdSituation'))
    role = db.relationship('Role',  backref="Users")
    situation = db.relationship('Situation', backref='Users')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.IdUser}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except TypeError :
            print('Type error in verify reset token') 
        except Exception as e :
            print("Error '{0}' occurred. Arguments {1}.".format(e.message, e.args))
        finally :
            if user_id is None :
                user_id = None
        return Users.query.get(user_id)
    def __repr__(self) :
        return f"Users('{self.IdUser}','{self.IdRole},'{self.FirstName}','{self.LastName}','{self.Email}','{self.PhoneNumber}','{self.Address}','{self.Pasword}','{self.CreatedAt}','{self.Enabled}')"        

    def get_id(self):
        return (self.IdUser)

class Farmer(db.Model):
    Idfarmer = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(250), nullable=True)
    LastName = db.Column(db.String(250), nullable=True)
    PhoneNumber = db.Column(db.String(250), nullable=True)
    Address = db.Column(db.String(250), nullable=True)
    Harvestime = db.Column(db.String(250), nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False) 

    def __repr__(self) :
        return f"Farmer('{self.Idfarmer}',{self.FirstName}','{self.LastName}','{self.PhoneNumber}','{self.Address}','{self.Harvestime}','{self.CreatedAt}')"        


class Agent(db.Model, UserMixin):
    IdAgent = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(250), nullable=True)
    LastName = db.Column(db.String(250), nullable=True)
    Password = db.Column(db.String(250), nullable=True)
    PhoneNumber = db.Column(db.String(250), nullable=True)
    Address = db.Column(db.String(250), nullable=True)
    IdService = db.Column(db.Integer , db.ForeignKey('service.IdService'))
    Enabled = db.Column(db.Integer, db.ForeignKey('situation.IdSituation'))
    Time = db.Column(db.Integer, db.ForeignKey('time.IdTime'))
    lat = db.Column(db.String(250), nullable=True)
    lon = db.Column(db.String(250), nullable=True)
    CreatedAt = db.Column(db.DateTime, nullable=False) 

    service = db.relationship('Service',  backref="Agent")
    time = db.relationship('Time',  backref="Agent")
    situation = db.relationship('Situation', backref='Agent')


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.IdAgent}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except TypeError :
            print('Type error in verify reset token') 
        except Exception as e :
            print("Error '{0}' occurred. Arguments {1}.".format(e.message, e.args))
        finally :
            if user_id is None :
                user_id = None
        return Agent.query.get(user_id)

    def __repr__(self) :
        return f"Agent('{self.IdAgent}',{self.FirstName}','{self.LastName}','{self.Password}','{self.PhoneNumber}','{self.Address}','{self.IdService}','{self.Time}','{self.lat}','{self.lon}','{self.CreatedAt}')"        

    def get_id(self):
        return (self.IdAgent)

   
class Priority(db.Model):
    IdPriority = db.Column(db.Integer, primary_key=True)
    PriorityName  = db.Column(db.String(250), nullable=False)
    CreatedAt  = db.Column(db.DateTime, nullable=False) 

    def __repr__(self) :
        return f"Priority('{self.IdPriority}','{self.PriorityName}','{self.CreatedAt}')"


class Situation(db.Model):
    IdSituation = db.Column(db.Integer, primary_key=True)
    Situation  = db.Column(db.String(250), nullable=False)
    CreatedAt  = db.Column(db.DateTime, nullable=False) 

    def __repr__(self) :
        return f"Situation('{self.IdSituation}','{self.Situation}','{self.CreatedAt}')"

class Time(db.Model):
    IdTime = db.Column(db.Integer, primary_key=True)
    TimeDec   = db.Column(db.String(250), nullable=False)
    CreatedAt  = db.Column(db.DateTime, nullable=False) 

    def __repr__(self) :
        return f"Time('{self.IdTime}','{self.TimeDec }','{self.CreatedAt}')"

class OrdersMaintenance(db.Model):
    IdOrder = db.Column(db.Integer, primary_key=True)
    OrderNumber = db.Column(db.String(250), nullable=True)
    FirstName  = db.Column(db.String(250), nullable=True)
    LastName   = db.Column(db.String(250), nullable=True)
    PhoneNumber = db.Column(db.String(250), nullable=True)
    Email = db.Column(db.String(250), nullable=True)
    Address  = db.Column(db.String(250), nullable=True)
    IdService  = db.Column(db.Integer, db.ForeignKey('service.IdService'))
    IdAgent = db.Column(db.Integer, db.ForeignKey('agent.IdAgent'))
    Price  = db.Column(db.String(250), nullable=True)
    IdPriority  = db.Column(db.Integer, db.ForeignKey('priority.IdPriority'))
    IdOrderStatus  = db.Column(db.Integer, db.ForeignKey('order_status.IdOrderStatus'))
    Ordertime = db.Column(db.String(250), nullable=True) 
    Time = db.Column(db.Integer, db.ForeignKey('time.IdTime')) 
    latit = db.Column(db.String(250), nullable=True)
    lon = db.Column(db.String(250), nullable=True)
    Comment = db.Column(db.String(250), nullable=True) 
    CreatedAt = db.Column(db.DateTime, nullable=False)

    service = db.relationship("Service", backref="OrdersMaintenance")
    priority = db.relationship("Priority", backref="OrdersMaintenance") 
    status = db.relationship("OrderStatus", backref="OrdersMaintenance") 
    time = db.relationship("Time", backref="OrdersMaintenance") 
    agent = db.relationship("Agent", backref="OrdersMaintenance") 


    def __repr__(self) :
        return f"OrdersMaintenance('{self.IdOrder}',{self.OrderNumber}','{self.FirstName}','{self.LastName}','{self.PhoneNumber}','{self.Email}','{self.IdService}','{self.Price}','{self.IdPriority}','{self.IdAgent}','{self.IdOrderStatus}','{self.Ordertime}','{self.Time}','{self.latit}','{self.lon}','{self.Comment}')"        

class OrderStatus(db.Model):
    IdOrderStatus = db.Column(db.Integer, primary_key=True)
    OrderStatus  = db.Column(db.String(250), nullable=False)
    CreatedAt  = db.Column(db.DateTime, nullable=False) 

    def __repr__(self) :
        return f"OrderStatus('{self.IdOrderStatus}','{self.OrderStatus}','{self.CreatedAt}')"


class OrdersCleaning(db.Model):
    IdOrder = db.Column(db.Integer, primary_key=True)
    OrderNumber = db.Column(db.String(250), nullable=True)
    FirstName  = db.Column(db.String(250), nullable=True)
    LastName   = db.Column(db.String(250), nullable=True)
    PhoneNumber = db.Column(db.String(250), nullable=True)
    Email = db.Column(db.String(250), nullable=True)
    Address  = db.Column(db.String(250), nullable=True)
    Service  = db.Column(db.String(250), nullable=True)
    Price  = db.Column(db.String(250), nullable=True)
    BookingType   = db.Column(db.Integer, nullable=True)
    IdOrderStatus  = db.Column(db.Integer, db.ForeignKey('order_status.IdOrderStatus'))
    Time = db.Column(db.String(250), nullable=True) 
    Maid = db.Column(db.String(250), nullable=True) 
    OrderDate = db.Column(db.String(250), nullable=True)
    Comment = db.Column(db.String(250), nullable=True) 
    CreatedAt = db.Column(db.DateTime, nullable=False)

    status = db.relationship("OrderStatus", backref="OrdersCleaning") 



    def __repr__(self) :
        return f"OrdersCleaning('{self.IdOrder}',{self.OrderNumber}','{self.FirstName}','{self.LastName}','{self.PhoneNumber}','{self.Email}','{self.Service}','{self.Price}','{self.Maid}','{self.OnceDate}','{self.BookingType}','{self.IdOrderStatus}','{self.Ordertime}','{self.Time}','{self.Comment}','{self.StartDate}','{self.EndDate}')"        
