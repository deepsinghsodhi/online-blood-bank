from application import db,app,login_manager
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True, nullable=False)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	role = db.Column(db.String(20),nullable = False)
	timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
	updation_date = db.Column(db.String(50),default="0")
	def __init__(self,  email,username, password,role):
		
		self.email = email
		self.username = username
		self.password = password
		self.role = role


	def __repr__(self):
		 return '{0},{1},{2},{3},{4}'.format(self.email,self.username,self.password,self.role,self.updation_date)
	 


class donor_details(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	d_id = db.Column(db.Integer, unique=True,nullable=False)
	name = db.Column(db.String(50),  nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	gender = db.Column(db.String(20),  nullable=False)
	dob = db.Column(db.DateTime(10))
	age = db.Column(db.Integer,nullable=False)
	blood_group = db.Column(db.String(20),  nullable=False)
	weight = db.Column(db.Integer,nullable=False)
	contact = db.Column(db.Integer, nullable=False)
	address = db.Column(db.String(100),  nullable=False)
	city = db.Column(db.String(50), nullable=False)
	state = db.Column(db.String(50), nullable=False)
	status = db.Column(db.String(20), default="Active")
	register_date = db.Column(db.DateTime,default=db.func.current_timestamp())
	updation_date = db.Column(db.String(50),default="0")
	donor_donate_relnshp = db.relationship('blood_stock', backref='donor_details', lazy='dynamic')
	
	def __init__(self, d_id,name,email,gender, dob,age,blood_group,weight,contact,address,city,state,status):
		self.d_id = d_id
		self.name = name
		self.email = email
		self.gender = gender
		self.dob = dob
		self.age = age
		self.blood_group = blood_group
		self.weight = weight
		self.contact = contact
		self.address = address
		self.city = city
		self.state = state
		self.status = status
		
	def __repr__(self):
		 return self.d_id,self.name,self.email,self.gender,self.dob,self.age,self.blood_group,self.weight,self.contact,self.address,self.city,self.state,self.status,self.register_date,self.updation_date


# -------------------------------Receipient Details--------------------------------------

class recipient_details(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	r_id = db.Column(db.Integer, unique=True,nullable=False)
	name = db.Column(db.String(50),  nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	gender = db.Column(db.String(20),  nullable=False)
	dob = db.Column(db.DateTime(10))
	age = db.Column(db.Integer,nullable=False)
	blood_group = db.Column(db.String(20),  nullable=False)
	weight = db.Column(db.Integer,nullable=False)
	contact = db.Column(db.Integer, nullable=False)
	address = db.Column(db.String(100),  nullable=False)
	city = db.Column(db.String(50), nullable=False)
	state = db.Column(db.String(50), nullable=False)
	status = db.Column(db.String(20), default="Active")
	register_date = db.Column(db.DateTime,default=db.func.current_timestamp())
	updation_date = db.Column(db.String(50),default="0")
	
	def __init__(self, r_id,name,email,gender, dob,age,blood_group,weight,contact,address,city,state,status):
		self.r_id = r_id
		self.name = name
		self.email = email
		self.gender = gender
		self.dob = dob
		self.age = age
		self.blood_group = blood_group
		self.weight = weight
		self.contact = contact
		self.address = address
		self.city = city
		self.state = state
		self.status = status
		
	def __repr__(self):
		 return self.r_id,self.name,self.email,self.gender,self.dob,self.age,self.blood_group,self.weight,self.contact,self.address,self.city,self.state,self.status,self.register_date,self.updation_date

# ----------------------------Staff details-----------------------------------------

class staff_details(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	s_id = db.Column(db.Integer, unique=True,nullable=False)
	name = db.Column(db.String(50),  nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	gender = db.Column(db.String(20),  nullable=False)
	dob = db.Column(db.DateTime(10))
	age = db.Column(db.Integer,nullable=False)
	contact = db.Column(db.Integer, nullable=False)
	address = db.Column(db.String(100),  nullable=False)
	city = db.Column(db.String(50), nullable=False)
	state = db.Column(db.String(50), nullable=False)
	status = db.Column(db.String(20), default="Active")
	register_date = db.Column(db.DateTime,default=db.func.current_timestamp())
	updation_date = db.Column(db.String(50),default="0")
	
	def __init__(self, s_id,name,email,gender, dob,age,contact,address,city,state,status):
		self.s_id = s_id
		self.name = name
		self.email = email
		self.gender = gender
		self.dob = dob
		self.age = age
		self.contact = contact
		self.address = address
		self.city = city
		self.state = state
		self.status = status
		
	def __repr__(self):
		 return self.s_id,self.name,self.email,self.gender,self.dob,self.age,self.contact,self.address,self.city,self.state,self.status,self.register_date,self.updation_date





# ----------------------------Receipient Deliver Blood---------------------------------------
class deliver_blood(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	r_id = db.Column(db.Integer,db.ForeignKey("recipient_details.r_id"))
	barcode_no = db.Column(db.String(100),nullable=False)
	blood_type = db.Column(db.String(5), nullable=False)
	quantity = db.Column(db.Integer,default='0')
	deliver_date = db.Column(db.DateTime,default=db.func.current_timestamp())

	def __init__(self, r_id,barcode_no,blood_type,quantity,storage_location):
		self.r_id = r_id
		self.barcode_no = barcode_no
		self.blood_type = blood_type
		self.quantity = quantity

	def __repr__(self):
		 return self.r_id,self.barcode_no,self.blood_type,self.quantity,self.deliver_date
	 
# --------------------------------------------------------------------------------------------


class blood_stock(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	d_id = db.Column(db.Integer,db.ForeignKey("donor_details.d_id"))
	barcode_no = db.Column(db.Integer,unique=True,nullable=False)
	blood_group = db.Column(db.String(50),  nullable=False)
	quantity = db.Column(db.Integer,default='0')
	storage_location = db.Column(db.String(50), nullable=False)
	date_of_collection = db.Column(db.DateTime,default=db.func.current_timestamp())
	expiry_date = db.Column(db.DateTime(10))

	def __init__(self,d_id,barcode_no,blood_group,quantity,storage_location,expiry_date):
		self.d_id = d_id
		self.barcode_no = barcode_no
		self.blood_group = blood_group
		self.quantity = quantity
		self.storage_location = storage_location
		self.expiry_date = expiry_date

	def __repr__(self):
		 return self.id,self.d_id,self.barcode_no,self.blood_group,self.quantity,self.storage_location,self.date_of_collection,self.expiry_date
	


class blood_request(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50),  nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	gender = db.Column(db.String(20),  nullable=False)
	age = db.Column(db.Integer,nullable=False)
	blood_group = db.Column(db.String(20),  nullable=False)
	weight = db.Column(db.Integer,nullable=False)
	contact = db.Column(db.Integer, nullable=False)
	address = db.Column(db.String(100),  nullable=False)
	city = db.Column(db.String(50), nullable=False)
	state = db.Column(db.String(50), nullable=False)
	status = db.Column(db.String(50), nullable=False)
	request_date = db.Column(db.DateTime,default=db.func.current_timestamp())
	approve_date = db.Column(db.String(50),default="0")
	
	def __init__(self,name,email,gender,age,blood_group,weight,contact,address,city,state,status):
	
		self.name = name
		self.email = email
		self.gender = gender
		self.age = age
		self.blood_group = blood_group
		self.weight = weight
		self.contact = contact
		self.address = address
		self.city = city
		self.state = state
		self.status = status
		
	def __repr__(self):
		 return self.name,self.email,self.gender,self.age,self.blood_group,self.weight,self.contact,self.address,self.city,self.state,self.status,self.request_date,self.approve_date

