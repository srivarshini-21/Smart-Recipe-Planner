from flask import Flask, render_template
from extensions import db, migrate, jwt, cors
from models import User, Recipe
from routes.auth import bp as auth_bp
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Flask app
app = Flask(__name__, template_folder='docs', static_folder='docs/static')

# App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Initialize extensions
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
cors.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp)

# Define routes for static pages
@app.route('/')
def login():
    return render_template('index.html')

@app.route('/signup.html')
def signup():
    return render_template('signup.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/categories.html')
def categories():
    return render_template('categories.html')

@app.route('/vegetarian.html')
def vegetarian():
    return render_template('vegetarian.html')

@app.route('/desserts.html')
def desserts():
    return render_template('desserts.html')

@app.route('/quickmeals.html')
def quickmeals():
    return render_template('quickmeals.html')

@app.route('/personalized.html')
def personalized():
    return render_template('personalized.html')

@app.route('/profile.html')
def profile():
    return render_template('profile.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
