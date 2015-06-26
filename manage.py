from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def index():
	return 'hello world'

@app.route('/hello/<name>')
def hello(name):
	return 'hello %s'%name

@app.route('/re')
def re():
	result = request.headers.get('user-agent')
	return result

if __name__ == '__main__':
	app.debug=True
	app.run()