from App.models import Recipe
from App.database import db

#controlelrs for recipe, we dont even think we gonna use these all 
def create_recipe(title, instructions, user_id, image):
    
    new_recipe = Recipe(title=title, instructions=instructions, user_id=user_id, image = image)
    db.session.add(new_recipe)
    db.session.flush()
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

def get_recipes_by_user(user_id, page, per_page, q, sort_by):
    query = Recipe.query.filter_by(user_id=user_id)

    if q:
        query = query.filter(
            db.or_(
                Recipe.title.ilike(f"%{q}%"),
                Recipe.instructions.ilike(f"%{q}%"),
                db.cast(Recipe.id, db.String).ilike(f"%{q}%")  
            )
        )

  
    if sort_by == 'id_asc':
        query = query.order_by(Recipe.id.asc())
    elif sort_by == 'id_desc':
        query = query.order_by(Recipe.id.desc())
    elif sort_by == 'title_desc':
        query = query.order_by(Recipe.title.desc())
    else:  
        query = query.order_by(Recipe.title.asc())
        

    return query.paginate(page=page, per_page=per_page)


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
