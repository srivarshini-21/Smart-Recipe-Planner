# Smart-Recipe-Planner
This project is a web application that helps users find recipes based on their available ingredients and dietary preferences. It also allows users to create an account, log in, and save their favorite recipes.

**Features:**
- User Authentication
- Save Personalized Recipes
- Responsive Design
- Profile Picture Updation

**Technologies Used:**
- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- Database: MySQL

## Project Structure

## Files and Directories

- `app.py`: The main application file where the Flask app is created and configured.
- `config.py`: Configuration file for the application settings.
- `delete_user.py`: Script to handle user deletion.
- `instance/`: Directory for instance-specific files.
- `migrations/`: Directory for database migration files managed by Alembic.
- `models.py`: File containing SQLAlchemy models.
- `routes/`: Directory containing route handlers.
  - `__init__.py`: Initialization file for the routes module.
  - `auth.py`: Authentication-related routes.
  - `recipes.py`: Recipe-related routes.
- `static/`: Directory for static files like JavaScript, CSS, and images.
- `templates/`: Directory for HTML templates.
- `venv/`: Virtual environment directory.

## Setup

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-directory>

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the dependencies:
   pip install -r requirements.txt

4. Set up the database:
   flask db upgrade  # Run database migrations
   flask run  # Start the server

### Usage
Use the provided routes to interact with the application.

### Example Routes

- **User Authentication**
  - `POST /login`: Logs in a user.
3. Make your changes.
4. Commit your changes (git commit -m 'Add user authentication feature').
  - `POST /register`: Registers a new user.
    - **Input**: JSON object with `username`, `email`, and `password`.
    - **Output**: JSON object with user details.

- **Recipe Management**
  - `GET /recipes`: Retrieves all recipes.
    - **Output**: JSON array of recipe objects.
  - `POST /recipes`: Adds a new recipe.
    - **Input**: JSON object with recipe details (e.g., `title`, `ingredients`, `instructions`).
    - **Output**: JSON object with the created recipe.
  - `PUT /recipes/<id>`: Updates an existing recipe.
    - **Input**: JSON object with updated recipe details.
    - **Output**: JSON object with the updated recipe.
  - `DELETE /recipes/<id>`: Deletes a recipe.
    - **Output**: JSON object with a success message.
Use the provided routes to interact with the application.
