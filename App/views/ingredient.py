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


@ingredient_views.route('/updateIngredient/<int:id>', methods=['GET'])
@jwt_required()
def show_ingredient_update_form(id):
    ingredient = get_user_ingredient(id)
    print("testing")
    if not ingredient or ingredient.user_id != current_user.id:
        return redirect(url_for('ingredient_views.ingredient_page'))

    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", default='', type=str)
    sort_by = request.args.get("sort_by", default='title_asc')

    paginated_ingredients = get_ingredients_by_user(current_user.id, page, 5, q, sort_by)
    ingredients_json = [i.get_json() for i in paginated_ingredients.items]

    return render_template(
        'ingredient.html',
        current_user=current_user,
        is_authenticated=True,
        ingredients=paginated_ingredients,
        ingredients_json=ingredients_json,
        ingredient_to_edit=ingredient,
        q=q,
        sort_by=sort_by
    )


@ingredient_views.route('/updateIngredient/<int:id>', methods=['POST'])
@jwt_required()
def update_ingredient(id):
    ingredient = get_user_ingredient(id)

    page = int(request.form.get("page", 1))
    q = request.form.get("q", '')
    sort_by = request.form.get("sort_by", default='title_asc')

    if not ingredient or ingredient.user_id != current_user.id:
        return redirect(url_for('ingredient_views.ingredient_page'))

    new_name = request.form.get('name')
    new_quantity = request.form.get('quantity')
    new_unit = request.form.get('unit')
    new_image = request.form.get('image')
    update_user_ingredient(ingredient.id, new_name, new_quantity, new_unit, new_image)

    flash("Ingredient updated successfully", "success")
    return redirect(url_for('ingredient_views.ingredient_page', page=page, q=q, sort_by=sort_by))