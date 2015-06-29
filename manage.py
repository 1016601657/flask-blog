from flask import Flask, render_template, session, redirect, url_for, flash
import os
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Shell,Manager
# from flask.ext.wtf import Form
# from wtforms import StringField, SubmitField
# from wtforms.validators import Required
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import request
from datetime import datetime
app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = \
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
# class NameForm():
# 	name = StringField('What is your name?', validators=[Required()])
# 	submit = SubmitField('submit,,')
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	def __repr__(self):
		return '<User %r>' % self.username
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	def __repr__(self):
		return '<Role %r>' % self.name
	users = db.relationship('User', backref='role')


class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
	name = None
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		old_name = session.get('name')
		if name is not None and name != old_name:
			flash('look likes you change you name')
		session['name'] = name
		return redirect(url_for('index'))
	return render_template('hello.html', form=form, name=session.get('name'))

@app.route('/hello/<name>')
def hello(name):
	names = {'Michaelaaa':90, 'Bob':80, 'Tracy':70}
	return render_template('index.html',names=names, current_time=datetime.utcnow())

@app.route('/re')
def re():
	result = request.headers.get('user-agent')
	return result

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
	app.debug=True
	manager.run()