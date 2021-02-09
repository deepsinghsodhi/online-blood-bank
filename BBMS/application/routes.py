from flask import render_template,redirect,url_for,request,flash
from application import app,db,bcrypt
from application.models import *
from datetime import timedelta

from flask_login import login_user,current_user,logout_user,login_required
# Import the decorators
from flask_permissions.decorators import user_is, user_has


# ----------------Error pages----------------------------------------------------------



################ Errors *****************
@app.errorhandler(401)
def error_401(error):
	return render_template('401.html'), 401


@app.errorhandler(404)
def error_404(error):
	return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(error):
	return render_template('500.html'), 500

# ------------------------------Home Route-----------------------------------------------------

@app.route('/')
@app.route('/home/')
def home():
		# Command to create database
		# db.create_all()
		# By default login credentials------
		# user = User('bbms','bbms@gmail.com','$2y$12$C3cXRZPO96RtWnIGheptKOi3l.NGMLnPDl5/mqX40jhSYzT4b9zzq','admin')
		# db.session.add(user)
		# db.session.commit()
		return render_template('home.html')

# --------------------------Register Page--------------------------------------
@app.route('/register/',methods=['GET','POST'])
def register():
	emailss = db.session.query(User.email).all()
	emails = [value for value, in emailss]
	
	if current_user.is_authenticated:
		return redirect(url_for('home'))
		
	if request.method == 'POST':
		reg_type = request.form['reg_type']
		r_id = request.form['id']
		username = request.form['username']
		name = request.form['name']
		email = request.form['email']
		contact = request.form['contact']
		gender = request.form['gender']
		dob = datetime.datetime.strptime(str(request.form['dob']), '%Y-%m-%d')
		# calculate age...
		# find current year
		c_year = datetime.datetime.today().year
		# calculate age
		age = c_year-int(dob.strftime('%Y'))  #convert datetime.date object into int type
		bg = request.form['bg']
		weight = request.form['weight']
		address = request.form['address']
		state = request.form['state']
		city = request.form['city']
		password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
		
		if email in emails:
			flash('Oops!! This Email IS alredy registered, Try New One','danger')
		else:
			if reg_type == 'donor':
				try:
					donor = donor_details(r_id,name,email,gender,dob,age,bg,weight,contact,address,city,state,'Active')
					user = User(email,username,password,'donor')
				
					db.session.add(donor)
					db.session.add(user)
					db.session.commit()
					flash('Congrats!! You are Successfully Registered you can login ','success')
					return redirect(url_for('login'))
				# except:
					# flash('Something went wrong!!','danger')
					# return redirect('/register/')
				except Exception as e:
					return(str(e))
				
			else:
				try:
					recipient = recipient_details(r_id,name,email,gender,dob,age,bg,weight,contact,address,city,state,'Active')
					user = User(email,username,password,'recipient')
				
					db.session.add(recipient)
					db.session.add(user)
					db.session.commit()
					flash('Congrats!! You are Successfully Registered you can login ','success')
					return redirect(url_for('login'))
				except:
					flash('Something went wrong!!','danger')
					return redirect('/register/')
				
			

	return render_template('register.html')
# ------------------------------Login Page Route-----------------------------------------------------

@app.route('/login/',methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))

	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		
		user = User.query.filter_by(email=email).first()
		print(user)
		if user and bcrypt.check_password_hash(user.password,request.form['password']):
			login_user(user)
			next_page = request.args.get('next')
			flash('Login successful!!Welcome to Home Page!!','success')
			return redirect(next_page) if next_page else  redirect(url_for('home'))
		else:
			flash('Login Unsuccessful!! ','danger')
	return render_template('login.html')
	


# -----------------------------Admin Logout-----------------------------------------------------------------

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))


# --------------------------------ADMIN SECTION-------------------------------------------------------------
# -----------------------------Admin Dashboard--------------------------------------------------------------

@app.route('/dashboard/')
@login_required
@user_is('admin')
def dashboard():
		
		return render_template('admin_dash.html')

# --------------------------------ADMIN SECTION-------------------------------------------------------------
# -----------------------------Donor Tab--------------------------------------------------------------

@app.route('/donor/')
@login_required
@user_is('admin')
def donor():
		
		return render_template('donor_tab.html')

# -----------------------------------Add Donor--------------------------------------

@app.route('/add_donor/',methods=['GET','POST'])
@login_required
@user_is('admin')
def add_donor():
		

	if request.method == 'POST':
		d_id = request.form['d_id']
		name = request.form['name']
		email = request.form['email']
		username = request.form['username']
		gender = request.form['gender']
		dob = datetime.datetime.strptime(str(request.form['dob']), '%Y-%m-%d')
		# calculate age...
		# find current year
		c_year = datetime.datetime.today().year
		# calculate age
		age = c_year-int(dob.strftime('%Y'))  #convert datetime.date object into int type
		bg = request.form['bg']
		weight = request.form['weight']
		contact = request.form['contact']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

		
		# validation for unique email
		# user = db.session.query(User).all()
		user = User.query.filter_by(email=email).all()
		for e in user:
			print(e.email)
			if email == e.email:
				flash('This Email is already Taken!! Try Another One','danger')
				return redirect('/add_donor/')
				

		donor = donor_details(d_id,name,email,gender,dob,age,bg,weight,contact,address,city,state,'Active')
		user = User(email,username,password,'donor')
		try:
			db.session.add(donor)
			db.session.add(user)
			db.session.commit()
			flash('Donor has been Added successfully!!','success')
			return redirect('/add_donor/')

		except:
			flash('This id is already Taken!! Try Another One','danger')
			return redirect('/add_donor/')
		# except Exception as e:
		# 	return(str(e))
		
	return render_template('add_donor.html')


# -----------------------------------Search Donor--------------------------------------

@app.route('/search_donor/',methods=['GET','POST'])
@login_required
@user_is('admin')
def search_donor():
		
		if request.method=='GET':
			return render_template('search_d.html')
	
		if request.method=='POST':
			#------------------ Searched Donor Details------------------------------------------
			if request.form['Sbtn'] == 'Search':
				d_id = request.form['d_id']
				data = donor_details.query.filter_by(d_id=d_id).all()
				print('Working')
				if data == []:
					flash('Donor Not found ! Plz Check ID','danger')
				
				return render_template('search_d.html',data = data)

		return render_template('search_d.html')


# -----------------------------------View All Donor--------------------------------------

@app.route('/view_all_donor/')
@login_required
def view_all_donor():

		details  = donor_details.query.order_by(donor_details.id).all()
		return render_template('view_all_donor.html',details=details)


# -----------------------------------Update Donor--------------------------------------

@app.route('/update_donor/',methods=['GET','POST'])
@login_required
@user_is('admin')
def update_donor():
		

	if request.method=='POST':
		if request.form['Sbtn'] == 'Get':

			# Fetch all data from database
			donor = donor_details.query.order_by(donor_details.id).all()
	
			d_id = request.form['d_id']
			data = donor_details.query.filter_by(d_id=d_id).all()
			if data == []:
				flash('Donor Id Not found','danger')
			
			return render_template('update_donor.html',data = data,donor=donor)

		elif request.form['Sbtn'] == 'Update':
			
			# Fetch all  donor_details from database
			donor = donor_details.query.order_by(donor_details.id).all()
	
			d_id = request.form['d_id']
			name = request.form['name']
			email = request.form['email']
			gender = request.form['gender']
			dob_i= request.form['dob']
			# ---------convert dob (type of string) into datetime to save it into database-----
			dob = datetime.datetime.strptime(dob_i, '%Y-%m-%d %H:%M:%S')
			# ------------------------------------------------------------
			# find current year
			c_year = datetime.datetime.today().year
			# calculate age
			age = c_year-int(dob.strftime('%Y'))  #convert datetime.date object into int type
			bg = request.form['bg']
			weight = request.form['weight']
			contact = request.form['contact']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			status = request.form['status']
			updation_date = datetime.datetime.now()
			
			try:
				donor_details.query.filter_by(d_id=d_id).update({donor_details.name:name})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.email:email})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.gender:gender})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.dob:dob})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.age:age})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.blood_group:bg})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.weight:weight})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.contact:contact})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.address:address})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.city:city})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.state:state})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.status:status})
				db.session.commit()
				donor_details.query.filter_by(d_id=d_id).update({donor_details.updation_date:updation_date})
				db.session.commit()
				
				flash('Donor updated  successfully','success')
			except:
				flash('There was a problem in Updating  this Donor','danger')
			# except Exception as e:
			# 	return(str(e))

			return render_template('update_donor.html',staff=staff)
		else:
			pass
		
	return render_template('update_donor.html')


# -----------------------------------Delete Donor--------------------------------------

@app.route('/delete_donor/',methods=['GET','POST'])
@login_required
@user_is('admin')
def delete_donor():
		
		if request.method == 'POST':

			d_id = request.form['d_id']
			donor = donor_details.query.filter_by(d_id=d_id).first()	
			
			if donor == None:
				flash('Donor ID Not found','danger')
				print('Working')
			else:
				# fetch user email
				email = db.session.query(donor_details.email).filter_by(d_id=d_id).all()
				print(email[0][0]) 
				user = User.query.filter_by(email=email[0][0]).first()

				db.session.delete(donor)
				db.session.delete(user)
				db.session.commit()
				flash('Donor deleted  successfully','success')
				
		return render_template('delete_donor.html')

# ------------------------------------Blood bAnk Stock Tab--------------------------------------------------------------

@app.route('/stock/')
@login_required
@user_is('admin')
def stock():
		
		return render_template('stock_tab.html')



# -----------------------------------Add Stock--------------------------------------

@app.route('/add_blood_pack/',methods=['GET','POST'])
@login_required
@user_is('admin')
def add_blood_pack():
		
		if request.method == 'POST':
			d_id = request.form['d_id']
			bn = request.form['bn']
			bg = request.form['bg']
			qty = request.form['qty']
			storage = request.form['storage']
			expiry_date =  datetime.datetime.now() + timedelta(days=35)

			pack = blood_stock(d_id,bn,bg,qty,storage,expiry_date)
			try:
				db.session.add(pack)
				db.session.commit()
				flash('Blood Pack has been Added successfully!!','success')
				return redirect('/add_blood_pack/')

			except:
				flash('This Barcode No is already Taken!! Try Another One','danger')
				return redirect('/add_blood_pack/')
			# except Exception as e:
			# 	return(str(e))
			


		return render_template('add_blood_pack.html')




# -----------------------------------View stock--------------------------------------

@app.route('/view_all_stock/')
@login_required
@user_is('admin')
def view_all_stock():
		
		details  =  blood_stock.query.order_by(blood_stock.id).all()		
		return render_template('view_all_stock.html',details=details)


# -----------------------------------Update stock--------------------------------------

@app.route('/update_stock/',methods=['GET','POST'])
@login_required
@user_is('admin')
def update_stock():
		
	if request.method=='POST':
		if request.form['Sbtn'] == 'Get':

			# Fetch all data from database
			packs = blood_stock.query.order_by(blood_stock.id).all()
	
			barcode = request.form['barcode']
			data = blood_stock.query.filter_by(barcode_no=barcode).all()
			if data == []:
				flash('Barcode no. Not found','danger')
			
			return render_template('update_stock.html',data = data,packs=packs)

		elif request.form['Sbtn'] == 'Update':
			
			# Fetch all  blood_stock from database
			packs = blood_stock.query.order_by(blood_stock.id).all()

			d_id = request.form['d_id']
			barcode = request.form['barcode']
			bg = request.form['bg']
			qty = request.form['qty']
			storage = request.form['storage']
			
			try:
				blood_stock.query.filter_by(barcode_no=barcode).update({blood_stock.d_id:d_id})
				db.session.commit()
				blood_stock.query.filter_by(barcode_no=barcode).update({blood_stock.barcode_no:barcode})
				db.session.commit()
				blood_stock.query.filter_by(barcode_no=barcode).update({blood_stock.blood_group:bg})
				db.session.commit()
				blood_stock.query.filter_by(barcode_no=barcode).update({blood_stock.quantity:qty})
				db.session.commit()
				blood_stock.query.filter_by(barcode_no=barcode).update({blood_stock.storage_location:storage})
				db.session.commit()
				
				
				flash('Stock updated  successfully','success')
			except:
				flash('There was a problem in Updating  this Blood Pack','danger')
			# except Exception as e:
			# 	return(str(e))

	return render_template('update_stock.html')


# -----------------------------------Delete pack from stock--------------------------------------

@app.route('/delete_blood_pack/',methods=['GET','POST'])
@login_required
@user_is('admin')
def delete_blood_pack():
		

		if request.method == 'POST':

			barcode_no = request.form['barcode_no']
			stock = blood_stock.query.filter_by(barcode_no=barcode_no).first()	
			
			if stock == None:
				flash('Barcode No Not found','danger')
				print('Working')
			else:
				
				db.session.delete(stock)
				db.session.commit()
				flash(' PAck deleted  successfully','success')
			
		return render_template('delete_blood_pack.html')


# -----------------------------Recipient Tab--------------------------------------------------------------

@app.route('/recipient/')
@login_required
@user_is('admin')
def recipient():
		
		return render_template('recipient_tab.html')


# -----------------------------------Add Recipient--------------------------------------

@app.route('/add_recipient/',methods=['GET','POST'])
@login_required
@user_is('admin')
def add_recipient():
		
	if request.method == 'POST':
		r_id = request.form['r_id']
		name = request.form['name']
		email = request.form['email']
		username = request.form['username']
		gender = request.form['gender']
		dob = datetime.datetime.strptime(str(request.form['dob']), '%Y-%m-%d')
		# calculate age...
		# find current year
		c_year = datetime.datetime.today().year
		# calculate age
		age = c_year-int(dob.strftime('%Y'))  #convert datetime.date object into int type
		bg = request.form['bg']
		weight = request.form['weight']
		contact = request.form['contact']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

		
		# validation for unique email
		# user = db.session.query(User).all()
		user = User.query.filter_by(email=email).all()
		for e in user:
			print(e.email)
			if email == e.email:
				flash('This Email is already Taken!! Try Another One','danger')
				return redirect('/add_recipient/')
				

		Recipient = recipient_details(r_id,name,email,gender,dob,age,bg,weight,contact,address,city,state,'Active')
		user = User(email,username,password,'recipient')
		try:
			db.session.add(Recipient)
			db.session.add(user)
			db.session.commit()
			flash('Recipient  has been Added successfully!!','success')
			return redirect('/add_recipient/')

		except:
			flash('This id is already Taken!! Try Another One','danger')
			return redirect('/add_recipient/')
		# except Exception as e:
		# 	return(str(e))
		
	return render_template('add_recipient.html')


# -----------------------------------Search Recipient--------------------------------------

@app.route('/search_recipient/',methods=['GET','POST'])
@login_required
@user_is('admin')
def search_recipient():
		
		if request.method=='GET':
			return render_template('search_recipient.html')
	
		if request.method=='POST':
			#------------------ Searched Patient Details------------------------------------------
			if request.form['Sbtn'] == 'Search':
				r_id = request.form['r_id']
				data = recipient_details.query.filter_by(r_id=r_id).all()
				print('Working')
				if data == []:
					flash('Recipient Not found ! Plz Check ID','danger')
				
				return render_template('search_recipient.html',data = data)

		return render_template('search_recipient.html')


# -----------------------------------View Recipient--------------------------------------

@app.route('/view_all_recipient/')
@login_required
@user_is('admin')
def view_all_recipient():
		
		details  = recipient_details.query.order_by(recipient_details.id).all()
		return render_template('view_all_recipient.html',details=details)


# -----------------------------------Update recipient--------------------------------------

@app.route('/update_recipient/',methods=['GET','POST'])
@login_required
@user_is('admin')
def update_recipient():
		

	if request.method=='POST':
		if request.form['Sbtn'] == 'Get':

			# Fetch all data from database
			recipient = recipient_details.query.order_by(recipient_details.id).all()
	
			r_id = request.form['r_id']
			data = recipient_details.query.filter_by(r_id=r_id).all()
			if data == []:
				flash('Recipient Not found','danger')
			
			return render_template('update_recipient.html',data = data,recipient=recipient)

		elif request.form['Sbtn'] == 'Update':
			
			# Fetch all  recipient_details from database
			recipient = recipient_details.query.order_by(recipient_details.id).all()
	
			r_id = request.form['r_id']
			name = request.form['name']
			email = request.form['email']
			gender = request.form['gender']
			dob_i= request.form['dob']
			# ---------convert dob (type of string) into datetime to save it into database-----
			dob = datetime.datetime.strptime(dob_i, '%Y-%m-%d %H:%M:%S')
			# ------------------------------------------------------------
			contact = request.form['contact']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			status = request.form['status']
			updation_date = datetime.datetime.now()
			
			try:
				recipient_details.query.filter_by(r_id=r_id).update({recipient_details.name:name})
				db.session.commit()
				recipient_details.query.filter_by(r_id=r_id).update({recipient_details.email:email})
				db.session.commit()
				recipient_details.query.filter_by(r_id=r_id).update({recipient_details.gender:gender})
				db.session.commit()
				recipient_details.query.filter_by(r_id=r_id).update({recipient_details.dob:dob})
				db.session.commit()
				recipient_details.query.filter_by(r_id=r_id).update({recipient_details.contact:contact})
				db.session.commit()
				recipient_details.query.filter_by(r_id=r_id).update({recipient_details.address:address})
				db.session.commit()
				recipient_details.query.filter_by(r_id=r_id).update({recipient_details.city:city})
				db.session.commit()
				recipient_details.query.filter_by(r_id=r_id).update({recipient_details.state:state})
				db.session.commit()
				recipient_details.query.filter_by(r_id=r_id).update({recipient_details.status:status})
				db.session.commit()
				recipient_details.query.filter_by(r_id=r_id).update({recipient_details.updation_date:updation_date})
				db.session.commit()
				
				flash('Recipient updated  successfully','success')
			except:
				flash('There was a problem in Updating  this Recipient','danger')

			return render_template('update_recipient.html',staff=staff)
		else:
			pass
		
	return render_template('update_recipient.html')


# -----------------------------------Delete recipient--------------------------------------

@app.route('/delete_recipient/',methods=['GET','POST'])
@login_required
@user_is('admin')
def delete_recipient():
		
		if request.method == 'POST':

			r_id = request.form['r_id']
			recipient = recipient_details.query.filter_by(r_id=r_id).first()	
			
			if recipient == None:
				flash('Recipient Not found','danger')
				print('Working')
			else:
				# fetch user email
				email = db.session.query(recipient_details.email).filter_by(r_id=r_id).all()
				print(email[0][0]) 
				user = User.query.filter_by(email=email[0][0]).first()

				db.session.delete(recipient)
				db.session.delete(user)
				db.session.commit()
				flash(' Recipient deleted  successfully','success')
				
		return render_template('delete_recipient.html')


# -----------------------------Staff Tab--------------------------------------------------------------

@app.route('/staff/')
@login_required
@user_is('admin')
def staff():
		
		return render_template('staff_tab.html')


# -----------------------------------Add staff--------------------------------------

@app.route('/add_staff/',methods=['GET','POST'])
@login_required
@user_is('admin')
def add_staff():
		
	if request.method == 'POST':
		s_id = request.form['s_id']
		name = request.form['name']
		email = request.form['email']
		username = request.form['username']
		gender = request.form['gender']
		dob = datetime.datetime.strptime(str(request.form['dob']), '%Y-%m-%d')
		# calculate age...
		# find current year
		c_year = datetime.datetime.today().year
		# calculate age
		age = c_year-int(dob.strftime('%Y'))  #convert datetime.date object into int type
		contact = request.form['contact']
		address = request.form['address']
		city = request.form['city']
		state = request.form['state']
		password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

		
		# validation for unique email
		# user = db.session.query(User).all()
		user = User.query.filter_by(email=email).all()
		for e in user:
			print(e.email)
			if email == e.email:
				flash('This Email is already Taken!! Try Another One','danger')
				return redirect('/add_staff/')
				

		Staff = staff_details(s_id,name,email,gender,dob,age,contact,address,city,state,'Active')
		user = User(email,username,password,'Staff')
		try:
			db.session.add(Staff)
			db.session.add(user)
			db.session.commit()
			flash('Staff Member has been Added successfully!!','success')
			return redirect('/add_staff/')

		except:
			flash('This id is already Taken!! Try Another One','danger')
			return redirect('/add_staff/')
		# except Exception as e:
		# 	return(str(e))
		
	return render_template('add_staff.html')


# -----------------------------------Search staff--------------------------------------

@app.route('/search_staff/',methods=['GET','POST'])
@login_required
@user_is('admin')
def search_staff():
		
		if request.method=='GET':
			return render_template('search_staff.html')
	
		if request.method=='POST':
			#------------------ Searched Patient Details------------------------------------------
			if request.form['Sbtn'] == 'Search':
				s_id = request.form['s_id']
				data = staff_details.query.filter_by(s_id=s_id).all()
				print('Working')
				if data == []:
					flash('Satff Member Not found ! Plz Check ID','danger')
				
				return render_template('search_staff.html',data = data)

		return render_template('search_staff.html')


# -----------------------------------View All staff--------------------------------------

@app.route('/view_all_staff/')
@login_required
@user_is('admin')
def view_all_staff():
		
		details  = staff_details.query.order_by(staff_details.id).all()
		return render_template('view_all_staff.html',details=details)


# -----------------------------------Update staff--------------------------------------

@app.route('/update_staff/',methods=['GET','POST'])
@login_required
@user_is('admin')
def update_staff():
		

	if request.method=='POST':
		if request.form['Sbtn'] == 'Get':

			# Fetch all data from database
			staff = staff_details.query.order_by(staff_details.id).all()
	
			s_id = request.form['s_id']
			data = staff_details.query.filter_by(s_id=s_id).all()
			if data == []:
				flash('Member Not found','danger')
			
			return render_template('update_staff.html',data = data,staff=staff)

		elif request.form['Sbtn'] == 'Update':
			
			# Fetch all Doctor staff_details from database
			staff = staff_details.query.order_by(staff_details.id).all()
	
			s_id = request.form['s_id']
			name = request.form['name']
			email = request.form['email']
			gender = request.form['gender']
			dob_i= request.form['dob']
			# ---------convert dob (type of string) into datetime to save it into database-----
			dob = datetime.datetime.strptime(dob_i, '%Y-%m-%d %H:%M:%S')
			# ------------------------------------------------------------
			contact = request.form['contact']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			status = request.form['status']
			updation_date = datetime.datetime.now()
			
			try:
				staff_details.query.filter_by(s_id=s_id).update({staff_details.name:name})
				db.session.commit()
				staff_details.query.filter_by(s_id=s_id).update({staff_details.email:email})
				db.session.commit()
				staff_details.query.filter_by(s_id=s_id).update({staff_details.gender:gender})
				db.session.commit()
				staff_details.query.filter_by(s_id=s_id).update({staff_details.dob:dob})
				db.session.commit()
				staff_details.query.filter_by(s_id=s_id).update({staff_details.contact:contact})
				db.session.commit()
				staff_details.query.filter_by(s_id=s_id).update({staff_details.address:address})
				db.session.commit()
				staff_details.query.filter_by(s_id=s_id).update({staff_details.city:city})
				db.session.commit()
				staff_details.query.filter_by(s_id=s_id).update({staff_details.state:state})
				db.session.commit()
				staff_details.query.filter_by(s_id=s_id).update({staff_details.status:status})
				db.session.commit()
				staff_details.query.filter_by(s_id=s_id).update({staff_details.updation_date:updation_date})
				db.session.commit()
				
				flash('Staff Member updated  successfully','success')
			except:
				flash('There was a problem in Updating  this Staff Member','danger')

			return render_template('update_staff.html',staff=staff)
		else:
			pass
		

	return render_template('update_staff.html')


# -----------------------------------Delete staff--------------------------------------

@app.route('/delete_staff/',methods=['GET','POST'])
@login_required
@user_is('admin')
def delete_staff():
		
		if request.method == 'POST':

			s_id = request.form['s_id']
			staff = staff_details.query.filter_by(s_id=s_id).first()	
			
			if staff == None:
				flash('Member Not found','danger')
				print('Working')
			else:
				# fetch user email
				email = db.session.query(staff_details.email).filter_by(s_id=s_id).all()
				print(email[0][0]) 
				user = User.query.filter_by(email=email[0][0]).first()

				db.session.delete(staff)
				db.session.delete(user)
				db.session.commit()
				flash('Staff Member deleted  successfully','success')
				
		return render_template('delete_staff.html')



# -----------------------------Admin Dashboard--------------------------------------------------------------

@app.route('/user/')
@login_required
@user_is('admin')
def user():
		
		return render_template('user_tab.html')




# -----------------------------------View All user--------------------------------------

@app.route('/view_all_user/')
@login_required
@user_is('admin')
def view_all_user():
		
		details  = User.query.order_by(User.id).all()
		return render_template('view_all_user.html',details=details)


# -----------------------------------Update user--------------------------------------

@app.route('/update_user/',methods=['GET','POST'])
@login_required
@user_is('admin')
def update_user():
		

	if request.method=='POST':
		if request.form['Sbtn'] == 'Get':

			# Fetch all User from database
			user = User.query.order_by(User.id).all()
	
			email = request.form['email']

			data = User.query.filter_by(email=email).all()
			if data == []:
				flash('User Not found','danger')
			
			return render_template('update_user.html',data = data,user=user)

		elif request.form['Sbtn'] == 'Update':
			
			# Fetch all User from database
			user = User.query.order_by(User.id).all()
			
			# Updatation From data
			email = request.form['email']
			username = request.form['username']
			password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
			updation_date = datetime.datetime.now()
			
			try:
				User.query.filter_by(email=email).update({User.email:email})
				db.session.commit()
				User.query.filter_by(email=email).update({User.username:username})
				db.session.commit()
				User.query.filter_by(email=email).update({User.password:password})
				db.session.commit()
				User.query.filter_by(email=email).update({User.updation_date:updation_date})
				db.session.commit()
			

				flash('User updated  successfully!!','success')
				return redirect(url_for('update_user'))
			except:
				flash('There was a problem in Updating  this User','danger')
				return redirect(url_for('update_user'))
			# except Exception as e:
		# 		return(str(e))

			return render_template('update_user.html',user=user)
		else:
			pass
		
	return render_template('update_user.html')


# -----------------------------------Delete user--------------------------------------

@app.route('/delete_user/',methods=['GET','POST'])
@login_required
@user_is('admin')
def delete_user():
		
		if request.method == 'POST':

			email = request.form['email']
			user = User.query.filter_by(email=email).first()	
			print('user')
			print(user)
			if user == []:
				flash('User Not found','danger')
			else:
				db.session.delete(user)
				db.session.commit()
				flash('User deleted  successfully','success')
				
		return render_template('delete_user.html')



# -----------------------------Settings--------------------------------------------------------------

@app.route('/settings/')
def settings():
		
		return render_template('settings.html')


# -----------------------------Profile--------------------------------------------------------------

@app.route('/profile/',methods=['GET','POST'])
def profile():
		
	if request.method == 'GET':
		if current_user.role == 'donor':
		
			email = current_user.email
			data = donor_details.query.filter_by(email=email).all()
			for d in data:
				u_id = d.d_id
			print(u_id)
			return render_template('profile.html',data=data,u_id = u_id)

		elif current_user.role == 'staff':
		
			email = current_user.email
			data = staff_details.query.filter_by(email=email).all()
			for d in data:
				u_id = d.s_id
			print(u_id)
			return render_template('profile.html',data=data,u_id = u_id)

		elif current_user.role == 'recipient':
		
			email = current_user.email
			data = recipient_details.query.filter_by(email=email).all()
			for d in data:
				u_id = d.r_id
			print(u_id)
			return render_template('profile.html',data=data,u_id = u_id)
		
		else:
			print('Nothing')
# -----------------------------------------------

	if request.method == 'POST':
		email = current_user.email
		if current_user.role == 'admin':
			username = request.form['username']
			updation_date = datetime.datetime.now()
			try:
				
				User.query.filter_by(email=email).update({User.username:username})
				db.session.commit()
				User.query.filter_by(email=email).update({User.updation_date:updation_date})
				db.session.commit()
				
				flash(' Profile Updated successfully','success')
				print("Updated")
				return redirect(url_for('profile'))
			except:
				flash('There was a problem in Updating  this Profile','danger')


		elif current_user.role == 'donor':
			username = request.form['username']
			name = request.form['name']
			email = request.form['email']
			gender = request.form['gender']
			dob_i= request.form['dob']
			# ---------convert dob (type of string) into datetime to save it into database-----
			dob = datetime.datetime.strptime(dob_i, '%Y-%m-%d %H:%M:%S')
			# ------------------------------------------------------------
			# find current year
			c_year = datetime.datetime.today().year
			# calculate age
			age = c_year-int(dob.strftime('%Y'))  #convert datetime.date object into int type
			bg = request.form['bg']
			weight = request.form['weight']
			contact = request.form['contact']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			status = request.form['status']
			updation_date = datetime.datetime.now()
			
			try:
				donor_details.query.filter_by(email=email).update({donor_details.name:name})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.email:email})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.gender:gender})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.dob:dob})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.age:age})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.blood_group:bg})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.weight:weight})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.contact:contact})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.address:address})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.city:city})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.state:state})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.status:status})
				db.session.commit()
				donor_details.query.filter_by(email=email).update({donor_details.updation_date:updation_date})
				db.session.commit()
				
				User.query.filter_by(email=email).update({User.username:username})
				db.session.commit()
				User.query.filter_by(email=email).update({User.updation_date:updation_date})
				db.session.commit()
				
				flash(' Profile Updated successfully','success')
				print("Updated")
				return redirect(url_for('profile'))
			except:
				flash('There was a problem in Updating  this Profile','danger')

		elif current_user.role == 'recipient':
			username = request.form['username']
			name = request.form['name']
			email = request.form['email']
			gender = request.form['gender']
			dob_i= request.form['dob']
			# ---------convert dob (type of string) into datetime to save it into database-----
			dob = datetime.datetime.strptime(dob_i, '%Y-%m-%d %H:%M:%S')
			# ------------------------------------------------------------
			# find current year
			c_year = datetime.datetime.today().year
			# calculate age
			age = c_year-int(dob.strftime('%Y'))  #convert datetime.date object into int type
			bg = request.form['bg']
			weight = request.form['weight']
			contact = request.form['contact']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			status = request.form['status']
			updation_date = datetime.datetime.now()
			
			try:
				recipient_details.query.filter_by(email=email).update({recipient_details.name:name})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.email:email})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.gender:gender})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.dob:dob})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.age:age})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.blood_group:bg})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.weight:weight})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.contact:contact})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.address:address})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.city:city})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.state:state})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.status:status})
				db.session.commit()
				recipient_details.query.filter_by(email=email).update({recipient_details.updation_date:updation_date})
				db.session.commit()
				
				User.query.filter_by(email=email).update({User.username:username})
				db.session.commit()
				User.query.filter_by(email=email).update({User.updation_date:updation_date})
				db.session.commit()
				
				flash(' Profile Updated successfully','success')
				print("Updated")
				return redirect(url_for('profile'))
			except:
				flash('There was a problem in Updating  this Profile','danger')


		elif current_user.role == 'staff':
			username = request.form['username']
			name = request.form['name']
			email = request.form['email']
			gender = request.form['gender']
			dob_i= request.form['dob']
			# ---------convert dob (type of string) into datetime to save it into database-----
			dob = datetime.datetime.strptime(dob_i, '%Y-%m-%d %H:%M:%S')
			# ------------------------------------------------------------
			# find current year
			c_year = datetime.datetime.today().year
			# calculate age
			age = c_year-int(dob.strftime('%Y'))  #convert datetime.date object into int type
			contact = request.form['contact']
			address = request.form['address']
			city = request.form['city']
			state = request.form['state']
			status = request.form['status']
			updation_date = datetime.datetime.now()
			
			try:
				staff_details.query.filter_by(email=email).update({staff_details.name:name})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.email:email})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.gender:gender})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.dob:dob})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.age:age})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.blood_group:bg})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.weight:weight})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.contact:contact})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.address:address})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.city:city})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.state:state})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.status:status})
				db.session.commit()
				staff_details.query.filter_by(email=email).update({staff_details.updation_date:updation_date})
				db.session.commit()
				
				User.query.filter_by(email=email).update({User.username:username})
				db.session.commit()
				User.query.filter_by(email=email).update({User.updation_date:updation_date})
				db.session.commit()
				
				flash(' Profile Updated successfully','success')
				print("Updated")
				return redirect(url_for('profile'))
			except:
				flash('There was a problem in Updating  this Profile','danger')

	return render_template('profile.html')


# -----------------------------Change Password--------------------------------------------------------------


@app.route('/change_password/',methods=['GET','POST'])
def change_password():
		
		if request.method == "POST":
			email = current_user.email
			password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
			updation_date = datetime.datetime.now()
			
			try:
				User.query.filter_by(email=email).update({User.password:password})
				db.session.commit()
				User.query.filter_by(email=email).update({User.updation_date:updation_date})
				db.session.commit()
			

				flash('Password updated  successfully!!','success')
				return redirect(url_for('change_password'))
			except:
				flash('There was a problem in Updating  Password, Try Again after Some time','danger')
				return redirect(url_for('change_password'))
			# except Exception as e:
		# 		return(str(e))

		return render_template('change_password.html')



@app.route('/user_dashboard/')
def user_dashboard():
		
		return render_template('user_dashboard.html')



@app.route('/search_donors/')
@login_required
def view_all_donor_user():

		details  = donor_details.query.order_by(donor_details.id).all()
		return render_template('view_all_donors.html',details=details)



@app.route('/blood_request/',methods=['GET','POST'])
def b_request():
	if request.method == 'GET':
		if current_user.role == 'donor':
		
			email = current_user.email
			data = donor_details.query.filter_by(email=email).all()
			for d in data:
				u_id = d.d_id
			print(u_id)
			return render_template('blood_request.html',data=data,u_id = u_id)

		elif current_user.role == 'staff':
		
			email = current_user.email
			data = staff_details.query.filter_by(email=email).all()
			for d in data:
				u_id = d.d_id
			print(u_id)
			return render_template('blood_request.html',data=data,u_id = u_id)

		elif current_user.role == 'recipient':
		
			email = current_user.email
			data = recipient_details.query.filter_by(email=email).all()
			for d in data:
				u_id = d.r_id
			print(u_id)
			return render_template('blood_request.html',data=data,u_id = u_id)
		
		else:
			print('Nothing')
# -----------------------------------------------

	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		u_id = request.form['u_id']
		name = request.form['name']
		gender = request.form['gender']
		age = request.form['age']
		bg = request.form['bg']
		weight = request.form['weight']
		contact = request.form['contact']
		address = request.form['address']
		city = request.form['city']

		state = request.form['state']
		status = request.form['status']
			

		req = blood_request(u_id,name,gender,age,bg,weight,contact,address,city,state,status)
	
		try:
			db.session.add(req)
			db.session.commit()

			flash(' Request Sent successfully','success')
			print("Updated")
			return redirect(url_for('b_request'))
		except:
			flash('There was a problem in Sending request','danger')
	

	return render_template('blood_request.html')


@app.route('/view_request/')
@login_required
def view_all_request():

		details  = blood_request.query.order_by(blood_request.id).all()
		return render_template('view_all_request.html',details=details)

