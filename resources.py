from flask import jsonify
from flask_restful import Resource

from models import Group, db


class GetGroups(Resource):

    def get(self):
        all_groups = []
        groups = db.session.query(Group).all()
        for group in groups:
            group_dict = {
                'id': group.id,
                'name': group.name,
            }
            all_groups.append(group_dict)
        return jsonify(all_groups)
