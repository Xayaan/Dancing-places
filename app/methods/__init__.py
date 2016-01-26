from app import app, db, models, login_manager
from app.models import core

login_manager.login_message = "Error. Try logging in first?"

@login_manager.user_loader
def load_user(userid):
	try:
		user = core.User.query.filter_by(id = userid).first()
		return user
	except:
		return None