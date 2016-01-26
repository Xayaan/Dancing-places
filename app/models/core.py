from app import db, app
from werkzeug import generate_password_hash, check_password_hash
import datetime, hashlib, uuid, flask.ext.whooshalchemy

ADMIN = 1
USER = 0

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(255))
	lastname = db.Column(db.String(255))
	email = db.Column(db.String(255), unique = True)
	user_status = db.Column(db.Integer)
	pwdhash = db.Column(db.String(255))
	salt = db.Column(db.String(255))

	def __init__(self, fullname, email, password):
		self.set_name(fullname)
		self.email = email
		self.salt = uuid.uuid4().hex
		if email in app.config['MASTER_EMAIL']:
			self.user_status = ADMIN
		else:
			self.user_status = USER
		self.set_password(password + self.salt)

	# Required for Client-Side Session Management

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return self.id

	# Required for Administrative Interface

	def __unicode__(self):
		return self.email

	def set_name(self, fullname):
		for i in fullname:
			if i != " ":
				try:
					int(i)
				except ValueError:
					pass
				else:
					raise Exception("Invalid Input")
		try:
			self.firstname, self.lastname = fullname.split(" ")
		except ValueError:
			self.firstname = fullname
			self.lastname = None

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		salt = uuid.uuid4().hex
		return check_password_hash(self.pwdhash, password + self.salt)

	def __repr__(self):
		return '<User %r>' % (self.email)


class Dance(db.Model):
	__tablename__ = 'dance'
	id = db.Column(db.Integer, primary_key = True)
	country = db.Column(db.String(255))
	city = db.Column(db.String(255))
	address = db.Column(db.Text())
	cost = db.Column(db.Integer())
	type_of_dance = db.Column(db.String())
	dress_code = db.Column(db.String())
	months = db.Column(db.String())
	website = db.Column(db.String())
	facebook = db.Column(db.String())
	twitter = db.Column(db.String())
	meetup = db.Column(db.String())
	contact_email = db.Column(db.String())
	notes = db.Column(db.Text())

	approved = db.Column(db.Boolean())

	def __repr__(self):
		return '<Dance %r>' % (self.id)
