from App.models import Ingredient
from App.database import db

#Controller for ingredients
def create_ingredient(name, quantity, user_id, image, unit):
    new_ingredient = Ingredient(name=name, quantity=quantity, user_id=user_id, image = image, unit = unit)
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient

def get_user_ingredient(id):
    return Ingredient.query.get(id)



def get_all_ingredients():
    return Ingredient.query.all()

def get_all_ingredients_json():
    ingredients = Ingredient.query.all()
    if not ingredients:
        return []
    return [ingredient.get_json() for ingredient in ingredients]

def get_ingredients_by_user(user_id, page, per_page, q, sort_by):
    query = Ingredient.query.filter_by(user_id=user_id)


    if q:
        search = f"%{q.lower()}%"
        query = query.filter(Ingredient.name.ilike(search))

  
    if sort_by == 'title_asc':
        query = query.order_by(Ingredient.name.asc())
    elif sort_by == 'title_desc':
        query = query.order_by(Ingredient.name.desc())
    elif sort_by == 'quantity_asc':
        query = query.order_by(Ingredient.quantity.asc())
    elif sort_by == 'quantity_desc':
        query = query.order_by(Ingredient.quantity.desc())
    elif sort_by == 'id_asc':
       query = query.order_by(Ingredient.id.asc())
    elif sort_by == 'id_desc':
        query = query.order_by(Ingredient.id.desc())
    else:
        query = query.order_by(Ingredient.name.asc())  
    return query.paginate(page=page, per_page=per_page)


def get_ingredients_by_user_json(user_id):
    ingredients = Ingredient.query.filter_by(user_id=user_id).all()
    return [ingredient.get_json() for ingredient in ingredients]

def update_user_ingredient(id, name, quantity, unit, image):
    ingredient = get_user_ingredient(id)
    if ingredient:
        if name:
            ingredient.name = name
        if quantity:
            ingredient.quantity = quantity
        if unit:
            ingredient.unit = unit
        if image:
            ingredient.image = image
        db.session.add(ingredient)
        db.session.commit()
        return ingredient
    return None

def delete_user_ingredient(id):
    ingredient = get_user_ingredient(id)
    if ingredient:
        db.session.delete(ingredient)
        db.session.commit()
        return True
    return False
