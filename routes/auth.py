from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from models import User, Recipe
from extensions import db

bp = Blueprint('auth', __name__)

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if user already exists
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"success": False, "message": "Username or email already taken"}), 400

    # Create new user
    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password, method='pbkdf2:sha256')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True, "message": "User created successfully!"}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid username or password"}), 401


@bp.route('/add_personalized_recipe', methods=['POST'])
@jwt_required()
def add_personalized_recipe():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    new_recipe = Recipe(
        name=data.get('name'),
        ingredients=data.get('ingredients'),
        instructions=data.get('instructions'),
        user_id=current_user_id
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"success": True, "message": "Recipe added successfully!"}), 201


@bp.route('/get_personalized_recipes', methods=['GET'])
@jwt_required()
def get_personalized_recipes():
    current_user_id = get_jwt_identity()
    recipes = Recipe.query.filter_by(user_id=current_user_id).all()
    recipes_data = [{'name': r.name, 'ingredients': r.ingredients, 'instructions': r.instructions} for r in recipes]
    return jsonify({'recipes': recipes_data}), 200
