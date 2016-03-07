import json
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        with open('static/first_snapshot.json') as data_file:
            data = json.load(data_file)
        return data

api.add_resource(HelloWorld, '/end')

if __name__ == "__main__":
    app.debug = True
    app.run(host='localhost')
    
#add /end to url to return json