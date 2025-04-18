from App.models import RecipeIngredients
from App.database import db

def add_ingredient_to_recipe(recipe_id, name, quantity):
    new_ingredient = RecipeIngredients(recipe_id=recipe_id, name=name, quantity=quantity)
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient

def get_ingredient(id):
    return RecipeIngredients.query.get(id)

def get_ingredients_by_recipe(recipe_id):
    return RecipeIngredients.query.filter_by(recipe_id=recipe_id).all()

def get_ingredients_by_recipe_json(recipe_id):
    ingredients = get_ingredients_by_recipe(recipe_id)
    return [i.get_json() for i in ingredients]

def update_ingredient(id, name=None, quantity=None):
    ingredient = get_ingredient(id)
    if ingredient:
        if name:
            ingredient.name = name
        if quantity:
            ingredient.quantity = quantity
        db.session.add(ingredient)
        db.session.commit()
        return ingredient
    return None

def delete_ingredient(id):
    ingredient = get_ingredient(id)
    if ingredient:
        db.session.delete(ingredient)
        db.session.commit()
        return True
    return False
