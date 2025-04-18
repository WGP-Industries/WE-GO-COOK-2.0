from App.models import Ingredient
from App.database import db

def create_ingredient(name, quantity, user_id, image):
    new_ingredient = Ingredient(name=name, quantity=quantity, user_id=user_id, image = image)
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient

def get_ingredient(id):
    return Ingredient.query.get(id)

def get_all_ingredients():
    return Ingredient.query.all()

def get_all_ingredients_json():
    ingredients = Ingredient.query.all()
    if not ingredients:
        return []
    return [ingredient.get_json() for ingredient in ingredients]

def get_ingredients_by_user(user_id):
    return Ingredient.query.filter_by(user_id=user_id).all()

def get_ingredients_by_user_json(user_id):
    ingredients = Ingredient.query.filter_by(user_id=user_id).all()
    return [ingredient.get_json() for ingredient in ingredients]

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
