from App.models import RecipeIngredient
from App.database import db

def add_ingredient_to_recipe(recipe_id, name, quantity, image):
    new_ingredient = RecipeIngredient(recipe_id=recipe_id, name=name, quantity=quantity, image= image)
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient

def get_ingredient(id):
    return RecipeIngredient.query.get(id)

def get_ingredients_by_recipe(recipe_id):
    return RecipeIngredient.query.filter_by(recipe_id=recipe_id).all()

def fetch_ingredients_for_recipes(recipes):
    for recipe in recipes:
        meal = getattr(recipe, "meal_data", None)
        if meal:
            for i in range(1, 21):
                name = meal.get(f"strIngredient{i}")
                quantity = meal.get(f"strMeasure{i}")
                if name and name.strip():
                    add_ingredient_to_recipe(
                        recipe_id=recipe.id,
                        name=name.strip(),
                        quantity=quantity.strip() if quantity else "",
                        image=""
                    )

def get_ingredients_by_recipe_json(recipe_id):
    ingredients = get_ingredients_by_recipe(recipe_id)
    return [i.get_json() for i in ingredients]

def update_ingredient_name(id, name=None):
    ingredient = get_ingredient(id)
    if ingredient:
        if name:
            ingredient.name = name
       
        db.session.add(ingredient)
        db.session.commit()
        return ingredient
    return None
def update_ingredient_quantity(id, quantity=None):
    ingredient = get_ingredient(id)
    if ingredient:
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
