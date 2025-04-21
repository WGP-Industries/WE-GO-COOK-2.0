from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers import *

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
@jwt_required(optional=True)
def index_page():
    user = current_user if current_user else None
    is_authenticated = user is not None

    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", default='', type=str)
    sort_by = request.args.get("sort_by", default='title_asc')

    if user:
        paginated_recipes = get_recipes_by_user(user.id, page, 5, q, sort_by)
        recipes_json = [r.get_json() for r in paginated_recipes.items]
    else:
        paginated_recipes = []
        recipes_json = [""]

    return render_template(
        'index.html',
        current_user=user,
        is_authenticated=is_authenticated,
        recipes=paginated_recipes,
        recipes_json=recipes_json,
        q=q, sort_by=sort_by,
        num_ingredients=1
    )


@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')


@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})


@index_views.route('/addRecipe', methods=['POST'])
@jwt_required()
def add_recipe():
    title = request.form.get('title')
    instructions = request.form.get('instructions')
    image = request.form.get('image') or ""
    user_id = current_user.id

    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", default='', type=str)
    sort_by = request.args.get("sort_by", default='title_asc')

    if not title or not instructions:
        flash("Missing required fields", "error")
        return redirect(url_for('index_views.index_page', page=page, q=q, sort_by = sort_by))

    recipe = create_recipe(title, instructions, user_id, image)

    num_ingredients = int(request.form.get('num-ingredients') or 1)

    for i in range(num_ingredients):
        name = request.form.get(f'ingredient_name_{i}') or "none"
        quantity = request.form.get(f'ingredient_quantity_{i}') or "0"
        unit = request.form.get(f'ingredient_unit_{i}') or "none"
        img = request.form.get(f'ingredient_image_{i}') or "none"
        if name and quantity:
            add_ingredient_to_recipe(recipe.id, name, quantity, img, unit)
    
    flash("Recipe added", "success")
    return redirect(url_for('index_views.index_page', page=page, q=q, sort_by = sort_by))


#We gotta make sure this works first
@index_views.route('/updateRecipe/<int:id>', methods=['GET'])
@jwt_required()
def show_update_form(id):
    recipe = get_recipe(id)

    if not recipe or recipe.user_id != current_user.id:
        return redirect(url_for('index_views.index_page'))

    # Get page and search query from URL parameters
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", default='', type=str)
    sort_by = request.args.get("sort_by", default='title_asc')


    # Fetch paginated recipe list for the current user
    paginated_recipes = get_recipes_by_user(current_user.id, page, 5, q, sort_by)
    recipes_json = [r.get_json() for r in paginated_recipes.items]

    return render_template(
        'index.html',
        current_user=current_user,
        is_authenticated=True,
        recipes=paginated_recipes,
        recipes_json=recipes_json,
        q=q,
        num_ingredients=len(get_ingredients_by_recipe(id)),
        ingredients_to_edit=get_ingredients_by_recipe(id),
        recipe_to_edit=recipe,
        sort_by = sort_by
    )


@index_views.route('/updateRecipe/<int:id>', methods=['POST'])
@jwt_required()
def update_recipe(id):
    recipe = get_recipe(id)

    page = int(request.form.get("page", 1))
    q = request.form.get("q", '')
    sort_by = request.args.get("sort_by", default='title_asc')

    if not recipe or recipe.user_id != current_user.id:
        return redirect(url_for('index_views.index_page'))

    # Update recipe title and instructions
    new_title = request.form.get('title')
    new_instructions = request.form.get('instructions')

    if not new_title or not new_instructions:
        return redirect(url_for('index_views.show_update_form', id=id, page = page, q=q, sort_by = sort_by))

    update_recipe_title(recipe.id, new_title)
    update_recipe_instructions(recipe.id, new_instructions)

    # Update ingredients
    ingredients = get_ingredients_by_recipe(recipe.id)

    for index, ingredient in enumerate(ingredients):
        name_key = f'ingredient_name_{index}'
        quantity_key = f'ingredient_quantity_{index}'
        image_key = f'ingredient_image_{index}'
        unit_key = f'ingredient_unit_{index}'

        new_name = request.form.get(name_key)
        new_quantity = request.form.get(quantity_key)
        new_image = request.form.get(image_key)
        new_unit = request.form.get(unit_key)

        if new_name:
            update_ingredient_name(ingredient.id, new_name)
        if new_quantity:
            update_ingredient_quantity(ingredient.id, new_quantity)
        if new_unit:
            update_ingredient_unit(ingredient.id, new_unit)
        if new_image is not None:
            update_ingredient_image(ingredient.id, new_image)

    flash("Recipe edited", "success")
    return redirect(url_for('index_views.index_page', page=page, q=q, sort_by = sort_by))
