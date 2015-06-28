from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    print 'hello world'

if __name__ == 'main':
    debug = True
    app.run()