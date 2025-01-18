from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__, template_folder='docs', static_folder='docs/static')

@app.route('/')
def login():
    return render_template('index.html')  # Render the 'index.html' template for the login page

@app.route('/signup.html')
def signup():
    return render_template('signup.html') 

# Define route for login page
@app.route('/home.html')
def home():
    return render_template('home.html')  # Render the 'login.html' template for the home page

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

# Define route for about page
@app.route('/about.html')
def about():
    return render_template('about.html')  # Render the 'about.html' template for the about page

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Import and register blueprints
from routes import auth, recipes
app.register_blueprint(auth.bp)
app.register_blueprint(recipes.bp)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
