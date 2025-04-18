from App.models import Recipe
from App.database import db

def create_recipe(title, instructions, user_id):
    new_recipe = Recipe(title=title, instructions=instructions, user_id=user_id)
    db.session.add(new_recipe)
    db.session.commit()
    return new_recipe

def get_recipe(id):
    return Recipe.query.get(id)

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

def update_recipe(id, title=None, instructions=None):
    recipe = get_recipe(id)
    if recipe:
        if title:
            recipe.title = title
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