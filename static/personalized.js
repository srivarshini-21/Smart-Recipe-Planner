document.getElementById('recipeForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting the traditional way

    const recipeName = document.getElementById('recipeName').value; // Corrected ID
    const ingredients = document.getElementById('ingredients').value;
    const instructions = document.getElementById('instructions').value;

    const recipe = { name: recipeName, ingredients: ingredients, instructions: instructions };
    const token = localStorage.getItem('access_token'); // Unified token key

    fetch('/add_personalized_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(recipe)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            loadPersonalizedRecipes(); // Reload recipes
            document.getElementById('recipeForm').reset(); // Corrected ID
        } else {
            alert("Failed to add recipe. Please try again.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    });
});

function loadPersonalizedRecipes() {
    const token = localStorage.getItem('access_token');
    fetch('/get_personalized_recipes', {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
    })
    .then(response => response.json())
    .then(data => {
        const recipeList = document.getElementById('recipe-list'); // Corrected ID
        recipeList.innerHTML = ''; // Clear previous recipes

        if (data.recipes && data.recipes.length > 0) {
            data.recipes.forEach(recipe => {
                const recipeDiv = document.createElement('div');
                recipeDiv.className = 'recipe';
                recipeDiv.innerHTML = `
                    <h3>Your Personalized Recipes</h3>
                    <h4>${recipe.name}</h4>
                    <p>Ingredients: ${recipe.ingredients}</p>
                    <p>Instructions: ${recipe.instructions}</p>
                `;
                recipeList.appendChild(recipeDiv);
            });
        } else {
            recipeList.innerHTML = "<p>No personalized recipes found.</p>";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("An error occurred while loading recipes.");
    });
}

document.addEventListener('DOMContentLoaded', loadPersonalizedRecipes);
