from flask import request, jsonify
import json

def swwagerRoutes(app, auxDB):
    @app.route('/swagger.json')
    def swagger():
        with open('swagger.json', 'r') as file:
            return jsonify(json.load(file))