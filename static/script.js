function likeRecipe(recipeName) {
    let favorites = localStorage.getItem('favoriteRecipes');
    if (!favorites) {
        favorites = [];
    } else {
        favorites = JSON.parse(favorites);
    }

    if (!favorites.includes(recipeName)) {
        favorites.push(recipeName);
        alert(recipeName + " has been added to your favorites!");
    } else {
        alert(recipeName + " is already in your favorites!");
    }

    localStorage.setItem('favoriteRecipes', JSON.stringify(favorites));
}
