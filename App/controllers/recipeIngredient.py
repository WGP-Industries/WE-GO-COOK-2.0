from App.models import RecipeIngredient
from App.database import db

#RecipeIngredient controller stuff
def add_ingredient_to_recipe(recipe_id, name, quantity, image, unit):
    new_ingredient = RecipeIngredient(recipe_id=recipe_id, name=name, quantity=quantity, image= image, unit = unit)
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient

def get_ingredient(id):
    return RecipeIngredient.query.get(id)

def get_ingredients_by_recipe(recipe_id):
    return RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()




def get_ingredients_by_recipe_json(recipe_id):
    ingredients = get_ingredients_by_recipe(recipe_id)
    return [i.get_json() for i in ingredients]

def update_ingredient_name(id, name):
    ingredient = get_ingredient(id)
    if ingredient:
        if name:
            ingredient.name = name
       
        db.session.add(ingredient)
        db.session.commit()
        return ingredient
    return None
def update_ingredient_quantity(id, quantity):

    ingredient = get_ingredient(id)
    if ingredient:
        if quantity:
            quantity = quantity
            ingredient.quantity = quantity
        db.session.add(ingredient)
        db.session.commit()
        return ingredient
    return 0

def update_ingredient_unit(id, unit):
    ingredient = get_ingredient(id)
    if ingredient:
        if unit:
            ingredient.unit = unit
        db.session.add(ingredient)
        db.session.commit()
        return ingredient
    return None

def update_ingredient_image(id, image):
    ingredient = get_ingredient(id)
    if ingredient and image is not None:
        ingredient.image = image
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
