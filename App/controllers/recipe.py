from App.models import Recipe
from App.database import db
import requests

def create_recipe(title, instructions, user_id, image):
    
    new_recipe = Recipe(title=title, instructions=instructions, user_id=user_id, image = image)
    db.session.add(new_recipe)
    db.session.flush()
    return new_recipe

def get_recipe(id):
    return Recipe.query.get(id)

def fetch_recipes():
    import requests
    response = requests.get("https://www.themealdb.com/api/json/v1/1/search.php?s")  
    
    if response.status_code == 200:
        data = response.json()
        meals = data.get("meals", [])
        recipes = []
        for meal in meals:
            title = meal.get("strMeal")
            instructions = meal.get("strInstructions")
            image = meal.get("strMealThumb")
            if title and instructions:
                recipe = create_recipe(
                    title=title,
                    instructions=instructions,
                    user_id=1,
                    image=image
                )
                recipe.meal_data = meal  # temporarily attach full meal data for later
                recipes.append(recipe)
        return recipes
    else:
        print("Failed to fetch recipes:", response.status_code)
        return []



def get_all_recipes():
    return Recipe.query.all()

def get_all_recipes_json():
    recipes = Recipe.query.all()
    if not recipes:
        return []
    return [recipe.get_json() for recipe in recipes]

def get_recipes_by_user(user_id):
    return Recipe.query.filter_by(user_id=user_id).all()

def get_recipes_by_user_json(user_id):
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    return [recipe.get_json() for recipe in recipes]

def update_recipe_title(id, title):
    recipe = get_recipe(id)
    if recipe:
        if title:
            recipe.title = title
      
        db.session.add(recipe)
        db.session.commit()
        return recipe
    return None

def update_recipe_instructions(id, instructions):
    recipe = get_recipe(id)
    if recipe:
        if instructions:
            recipe.instructions = instructions
        db.session.add(recipe)
        db.session.commit()
        return recipe
    return None

def delete_recipe(id):
    recipe = get_recipe(id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return True
    return False