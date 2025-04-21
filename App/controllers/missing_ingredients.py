from App.models import Recipe, Ingredient
from sqlalchemy.orm import joinedload

def get_recipes_missing_ingredients(user_id):
    user_ingredients = Ingredient.query.filter_by(user_id=user_id).all()
    user_stock = {ing.name.strip().lower(): ing.quantity for ing in user_ingredients}

    recipes_with_missing = []

    recipes = Recipe.query.options(joinedload(Recipe.ingredients)).all()

    for recipe in recipes:
        missing_ingredients = []

        for ri in recipe.ingredients:
            name = ri.name.strip().lower()
            required_qty = ri.quantity
            user_qty = user_stock.get(name, 0)
            if user_qty < required_qty:
                missing_ingredients.append({
                    'name': ri.name,
                    'required': required_qty,
                    'available': user_qty,
                    'unit': ri.unit,
                    'image': ri.image
                })

        if missing_ingredients:
            recipes_with_missing.append({
                'recipe': recipe,
                'missing_ingredients': missing_ingredients
            })

    return recipes_with_missing
