from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Recipe
from app import db

bp = Blueprint('recipes', __name__)

@bp.route('/', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'category': r.category,
        'image': r.image
    } for r in recipes]), 200

@bp.route('/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify({
        'id': recipe.id,
        'name': recipe.name,
        'ingredients': recipe.ingredients,
        'instructions': recipe.instructions,
        'category': recipe.category,
        'image': recipe.image
    }), 200

@bp.route('/get_personalized_recipes', methods=['GET'])
@jwt_required()
def get_personalized_recipes():
    try:
        user_id = get_jwt_identity()  # Get the logged-in user's ID from the JWT
        recipes = Recipe.query.filter_by(user_id=user_id).all()  # Query the database for the user's recipes
        
        # Convert recipes to a list of dictionaries
        recipes_data = [
            {
                "id": recipe.id,
                "name": recipe.name,
                "ingredients": recipe.ingredients,
                "instructions": recipe.instructions
            }
            for recipe in recipes
        ]

        return jsonify({"recipes": recipes_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

