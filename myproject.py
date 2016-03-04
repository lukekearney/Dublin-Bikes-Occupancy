from flask import Flask
import src
application = Flask(__name__)

@application.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@application.route("/about")
def about():
    return "BLUH"

if __name__ == "__main__":
    application.run(host='0.0.0.0')
