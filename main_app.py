from flask import Flask
from flask_restful import Api

from resources_queries import GetGroups, GetStudents, GetCourses

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
api = Api(app)

version = 'v1'

api.add_resource(GetGroups, f'/api/{version}/groups')
api.add_resource(GetStudents, f'/api/{version}/students')
api.add_resource(GetCourses, f'/api/{version}/courses')

if __name__ == '__main__':
    app.run(debug=True)
