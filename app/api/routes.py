from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Health, health_schema, healths_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some': 'value'}

@api.route('/health', methods = ['POST'])
@token_required
def create_health(current_user_token):
    allergies = request.json['allergies']
    weight = request.json['weight']
    height = request.json['height']
    pain_level = request.json['pain_level']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    health = Health(allergies, weight, height, pain_level, user_token=user_token) # Notice the `user_token` value in the new Health instance.
    
    db.session.add(health)
    db.session.commit()

    response = health_schema.dump(health)
    return jsonify(response)

@api.route('/health', methods = ['GET'])
@token_required
def get_health(current_user_token):
    a_user = current_user_token.token
    health = Health.query.filter_by(user_token = a_user).all()
    response = healths_schema.dump(health)
    return jsonify(response)

    
@api.route('/health/<id>', methods = ['GET'])
@token_required
def get_single_health(current_user_token, id):
    health = Health.query.get(id)
    response = health_schema.dump(health)
    return jsonify(response)

@api.route('/health/<id>', methods = ['POST', 'PUT'])
@token_required
def update_health(current_user_token, id):
    health = Health.query.get(id)
    health.allergies = request.json['allergies']
    health.weight = request.json['weight']
    health.height = request.json['height']
    health.pain_level = request.json['pain_level']
    health.user_token = current_user_token.token

    db.session.commit()
    response = health_schema.dump(health)
    return jsonify(response)

@api.route('/health/<id>', methods = ['DELETE'])
@token_required
def delete_health(current_user_token, id):
    health = Health.query.get(id)
    db.session.delete(health)
    
    db.session.commit()
    response = health_schema.dump(health)
    return jsonify(response)