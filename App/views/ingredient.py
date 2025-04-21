from flask import Blueprint, flash, redirect, render_template, request, send_from_directory, jsonify, url_for

from flask_jwt_extended import jwt_required, current_user
ingredient_views = Blueprint('ingredient_views', __name__, template_folder='../templates')

from App.controllers import (
     get_ingredients_by_user, update_user_ingredient,
     create_ingredient,  get_user_ingredient,  delete_user_ingredient
)

@ingredient_views.route('/ingredient', methods=['GET'])
@jwt_required(optional=True)
def ingredient_page():
    user = current_user if current_user else None
    is_authenticated = user is not None

    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", default='', type=str)
    sort_by = request.args.get("sort_by", default='title_asc')

    if user:
        paginated_ingredients = get_ingredients_by_user(user.id, page, 5, q, sort_by)
 
        ingredients_json = [i.get_json() for i in paginated_ingredients.items]
    else:

        paginated_ingredients = [""]
        ingredients_json = [""]

    return render_template(
        'ingredient.html',
        current_user=user,
        is_authenticated=is_authenticated,
        ingredients=paginated_ingredients,
        ingredients_json=ingredients_json,
        q=q,
        sort_by=sort_by,
        num_ingredients=len(ingredients_json)
    )


# route to add ingredient
@ingredient_views.route('/addingredient', methods=['POST'])
@jwt_required()
def add_ingredient():
    name = request.form.get('name')
    quantity = request.form.get('quantity')
    unit = request.form.get('unit')
    image = request.form.get('image') or ""
    user_id = current_user.id

    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", default='', type=str)
    sort_by = request.args.get("sort_by", default='title_asc')

    if not name or not quantity or not unit:
        flash("Missing required fields", "error")
        return redirect(url_for('ingredient_views.ingredient_page', page=page, q=q, sort_by=sort_by))

    
    ingredient = create_ingredient(name=name, quantity=quantity, unit=unit, image=image, user_id=user_id)


    flash("Ingredient added", "success")
    return redirect(url_for('ingredient_views.ingredient_page', page=page, q=q, sort_by=sort_by))