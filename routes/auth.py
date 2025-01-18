from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Recipe, User
from app import db

bp = Blueprint('auth', __name__)

@bp.route('/signup', methods=['POST'])  # Update to '/signup'
def signup():
    data = request.get_json()  # Get the data sent from the frontend
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if the user already exists
    user_exists = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"success": False, "message": "Username or email already taken"}), 400

    # Hash the password before storing using pbkdf2:sha256
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # Create a new user
    new_user = User(username=username, email=email, password_hash=hashed_password)

    # Add the new user to the database
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
    return jsonify({"msg": "Invalid email or password"}), 401

# Route for adding a personalized recipe
@bp.route('/add_personalized_recipe', methods=['POST'])
@jwt_required()  # Ensure the user is logged in
def add_personalized_recipe():
    current_user_id = get_jwt_identity()  # Get the ID of the logged-in user
    data = request.get_json()

    # Debugging log to verify the data received
    print(f"Received data: {data}")

    # Extract recipe details
    name = data.get('name')
    ingredients = data.get('ingredients')
    instructions = data.get('instructions')

    # Create the new recipe object
    new_recipe = Recipe(name=name, ingredients=ingredients, instructions=instructions, user_id=current_user_id)

    # Add the new recipe to the database
    try:
        db.session.add(new_recipe)
        db.session.commit()
        print("Recipe added successfully!")
    except Exception as e:
        print(f"Error adding recipe: {e}")

    return jsonify({"success": True, "message": "Recipe added successfully!"}), 201


# Route for fetching personalized recipes for the logged-in user
@bp.route('/get_personalized_recipes', methods=['GET'])
@jwt_required()
def get_personalized_recipes():
    try:
        user_id = get_jwt_identity()  # Retrieve user identity
        recipes = Recipe.query.filter_by(user_id=user_id).all()
        recipes_data = [{'name': r.name, 'ingredients': r.ingredients, 'instructions': r.instructions} for r in recipes]
        return jsonify({'recipes': recipes_data}), 200
    except Exception as e:
        print(f"Error in /get_personalized_recipes: {e}")
        return jsonify({'error': 'Internal server error'}), 500
    
@bp.route('/get_user_profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()  # Get the logged-in user's ID
    user = User.query.get(user_id)  # Fetch the user from the database

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Construct full path for the profile picture
    profile_picture_path = f"static/{user.profile_picture}" if user.profile_picture else "../static/default-profile-pic.jpeg"

    return jsonify({
        "success": True,
        "username": user.username,
        "profile_picture": profile_picture_path
    }), 200




@bp.route('/save_profile_pic', methods=['POST'])
@jwt_required()
def save_profile_pic():
    user_id = get_jwt_identity()
    data = request.get_json()
    profile_picture = data.get('profile_picture')

    if not profile_picture:
        return jsonify({"success": False, "message": "No profile picture selected"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Update the profile picture path in the database
    user.profile_picture = f"{profile_picture}"  # Save only the filename
    db.session.commit()

    print(f"Profile picture updated for user {user.username}: {profile_picture}")
    return jsonify({"success": True, "message": "Profile picture uploaded successfully"}), 200







