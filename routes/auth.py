from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from models import User, Recipe
from routes.extensions import db

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
        access_token = create_access_token(identity=str(user.id))  # Cast user.id to string
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Invalid username or password"}), 401


@bp.route('/add_personalized_recipe', methods=['POST'])
@jwt_required()
def add_personalized_recipe():
    try:
        current_user_id = get_jwt_identity()
        print(f"Current user ID: {current_user_id}")  # Debugging line
        data = request.get_json()
        print(f"Received data: {data}")  # Debugging line
        if not data:
            raise ValueError("No data provided")
        if not all(key in data for key in ('name', 'ingredients', 'instructions')):
            raise ValueError("Missing required fields")
        new_recipe = Recipe(
            name=data.get('name'),
            ingredients=data.get('ingredients'),
            instructions=data.get('instructions'),
            user_id=current_user_id
        )
        db.session.add(new_recipe)
        db.session.commit()
        return jsonify({"success": True, "message": "Recipe added successfully!"}), 201
    except Exception as e:
        current_app.logger.error(f"Error adding personalized recipe: {e}")
        return jsonify({"error": f"Unable to add recipe: {str(e)}"}), 422

@bp.route('/get_personalized_recipes', methods=['GET'])
@jwt_required()
def get_personalized_recipes():
    try:
        current_user_id = get_jwt_identity()
        print(f"Current user ID: {current_user_id}")  # Debugging line
        recipes = Recipe.query.filter_by(user_id=current_user_id).all()
        recipes_data = [{'name': r.name, 'ingredients': r.ingredients, 'instructions': r.instructions} for r in recipes]
        print(f"Fetched recipes: {recipes_data}")  # Debugging line
        return jsonify({'recipes': recipes_data}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching personalized recipes: {e}")
        return jsonify({"error": f"Unable to fetch recipes: {str(e)}"}), 422

# Fetch user profile data
@bp.route('/get_user_profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        return jsonify({
            "success": True,
            "username": user.username,
            "profile_picture": user.profile_picture
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching user profile: {e}")
        return jsonify({"success": False, "message": "Unable to fetch profile data"}), 500

# Save selected profile picture
@bp.route('/save_profile_pic', methods=['POST'])
@jwt_required()
def save_profile_pic():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        profile_picture = data.get("profile_picture")
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404
        
        user.profile_picture = profile_picture
        db.session.commit()
        
        return jsonify({"success": True, "message": "Profile picture updated successfully!"}), 200
    except Exception as e:
        current_app.logger.error(f"Error saving profile picture: {e}")
        return jsonify({"success": False, "message": "Unable to save profile picture"}), 500


