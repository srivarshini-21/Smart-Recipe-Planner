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
        user_id = get_jwt_identity()
        recipes = Recipe.query.filter_by(user_id=user_id).all()

        # Debugging log to check the recipes fetched
        print(f"Fetched recipes: {recipes}")

        recipes_data = [{'name': r.name, 'ingredients': r.ingredients, 'instructions': r.instructions} for r in recipes]
        return jsonify({'recipes': recipes_data}), 200
    except Exception as e:
        print(f"Error in /get_personalized_recipes: {e}")
        return jsonify({'error': 'Internal server error'}), 500


