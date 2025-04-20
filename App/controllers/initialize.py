from .user import *
from .recipe import *

from .ingredient import * 
from .recipeIngredient import *
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_ingredient(
    name="Sausage",
    image="https://www.gettyimages.com/photos/raw-sausage", 
    quantity="2 links",
    user_id=1  
)
        # Fetch recipes and store the returned list
    recipes = fetch_recipes()

    # Use that list to fetch and add ingredients
    fetch_ingredients_for_recipes(recipes)

    # Create the recipe directly with all fields
    # recipe = create_recipe(
    #     title="Spaghetti Carbonara",
    #     image="https://example.com/spaghetti.jpg",
    #     instructions="Boil pasta. Cook bacon. Mix with eggs and cheese. Combine.",
    #     user_id= 1
    # )
    # recipe = create_recipe(
    #     title="Spaghetti Carbonara",
    #     image="https://example.com/spaghetti.jpg",
    #     instructions="Boil pasta. Cook bacon. Mix with eggs and cheese. Combine.",
    #     user_id= 1
    # )
    # recipe = create_recipe(
    #     title="Spaghetti Carbonara",
    #     image="https://example.com/spaghetti.jpg",
    #     instructions="Boil pasta. Cook bacon. Mix with eggs and cheese. Combine.",
    #     user_id= 1
    # )
    # recipe = create_recipe(
    #     title="Spaghetti Carbonara",
    #     image="https://example.com/spaghetti.jpg",
    #     instructions="Boil pasta. Cook bacon. Mix with eggs and cheese. Combine.",
    #     user_id= 1
    # )

    # # Add ingredients directly
    # add_ingredient_to_recipe(
    #     recipe_id=recipe.id,
    #     name="Spaghetti",
    #     quantity="200g",
    #     image="https://example.com/spaghetti.png"
    # )

    # add_ingredient_to_recipe(
    #     recipe_id=recipe.id,
    #     name="Bacon",
    #     quantity="100g",
    #     image="https://example.com/bacon.png"
    # )

    # add_ingredient_to_recipe(
    #     recipe_id=recipe.id,
    #     name="Eggs",
    #     quantity="2",
    #     image=""
    # )

    # add_ingredient_to_recipe(
    #     recipe_id=recipe.id,
    #     name="Parmesan",
    #     quantity="50g",
    #     image=""
    # )