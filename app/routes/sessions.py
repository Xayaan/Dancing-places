from app import app, forms, models, db
from flask import render_template, request, jsonify, redirect, url_for, session
from flask.ext.login import LoginManager, login_user, current_user, logout_user, login_required
import random

@app.route('/', methods=['GET', 'POST'])
def user_home():
	r = lambda: random.randint(0,255)
	dances = models.core.Dance.query.all()
	color = '#%02X%02X%02X' % (r(),r(),r())
	return render_template("dashboard.html", color = color, dances = dances)

@app.route("/xyz", methods=['GET','POST'])
def home():
	if current_user.is_anonymous():
		r = lambda: random.randint(0,255)
		color = '#%02X%02X%02X' % (r(),r(),r())
		form = forms.sessions.UserRegisterForm()

		if request.method == "GET":
			return render_template("home.html", color = color, form = form)
		else:
			user = models.core.User(fullname = form.fullname.data, email = form.email.data, password = form.password.data)
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect(url_for('dashboard'))
	else:
		return redirect(url_for('dashboard'))

@app.route("/login", methods=['GET','POST'])
def login():
	if current_user.is_anonymous():
		r = lambda: random.randint(0,255)
		color = '#%02X%02X%02X' % (r(),r(),r())
		form = forms.sessions.LoginForm()

		if request.method == "GET":
			return render_template("login.html", color = color, form = form)
		else:
			user = models.core.User.query.filter_by(email = form.email.data).first()
			if user and user.check_password(form.password.data):
				login_user(user)
				return redirect(url_for('dashboard'))
			else:
				error = "Error. Try filling all the details correctly."
				return render_template('login.html', form = form, error = error)
	else:
		return redirect(url_for('dashboard'))

@app.route("/dance/add", methods=['GET','POST'])
def dance_add():
	dance_request = models.core.Dance(country = request.args.get('country', '0'), city = request.args.get('city', '0'), address = request.args.get('address', '0'), cost = request.args.get('cost', '0'), type_of_dance = request.args.get('dance_type', '0'), dress_code = request.args.get('dress', '0'), months = request.args.get('months', '0'), website = request.args.get('website', '0'), facebook = request.args.get('facebook', '0'), twitter = request.args.get('twitter', '0'), meetup = request.args.get('meetup', '0'), contact_email = request.args.get('contact', '0'), notes = request.args.get('notes', '0'), approved = False)

	db.session.add(dance_request)
	db.session.commit()
	return jsonify(string = "200 OK", object_id = dance_request.id)

@app.route("/dance/approve", methods=['GET','POST'])
@login_required
def dance_approve():
	dance_request = models.core.Dance.query.filter_by(id = request.args.get('object_id', '0')).first()
	dance_request.approved = True
	db.session.commit()
	return jsonify(string = "200 OK", object_id = dance_request.id, type = dance_request.type_of_dance, country = dance_request.country, city = dance_request.city, address = dance_request.address, dress = dance_request.dress_code, cost = dance_request.cost)

@app.route("/dance/delete", methods=['GET','POST'])
@login_required
def dance_cancel():
	dance_request = models.core.Dance.query.filter_by(id = request.args.get('object_id', '0')).first()
	db.session.delete(dance_request)
	db.session.commit()
	return jsonify(string = "200 OK")

@app.route("/dashboard", methods=['GET','POST'])
@login_required
def dashboard():
	r = lambda: random.randint(0,255)
	dances = models.core.Dance.query.all()
	color = '#%02X%02X%02X' % (r(),r(),r())
	return render_template("admin_dashboard.html", user = current_user, color = color, dances = dances)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('home'))
