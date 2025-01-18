from app import app, db  # Import your Flask app and the database
from models import User  # Replace `models` with the correct module for your User model

def delete_user_by_id(user_id):
    with app.app_context():  # Ensure the application context is active
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"User with ID {user_id} deleted successfully.")
        else:
            print("User not found.")

if __name__ == "__main__":
    try:
        user_id_to_delete = int(input("Enter the User ID to delete: "))
        delete_user_by_id(user_id_to_delete)
    except ValueError:
        print("Please enter a valid numeric User ID.")
