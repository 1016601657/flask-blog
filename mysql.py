from flask import Flask
from flask.ext.script import Shell
from flask.ext.script import Manager

app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def hello():
    return 'gaga'

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()