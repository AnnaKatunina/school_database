from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from resources import GetGroups

app = Flask(__name__)
api = Api(app)


version = 'v1'

api.add_resource(GetGroups, f'/api/{version}/groups')

if __name__ == '__main__':
    app.run(debug=True)
