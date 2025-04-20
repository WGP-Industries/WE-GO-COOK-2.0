<<<<<<< HEAD
from flask import Blueprint, flash, redirect, render_template, request, send_from_directory, jsonify, url_for
=======
from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers import create_user, initialize
>>>>>>> 2f67087418dbf7099b8153d59d01a86a0b869aac

from flask_jwt_extended import jwt_required, current_user
index_views = Blueprint('index_views', __name__, template_folder='../templates')


from App.controllers import (
    create_user, initialize, get_all_recipes,
    create_recipe, create_ingredient, 
    add_ingredient_to_recipe, get_all_recipes_json, get_recipes_by_user,get_recipe,  get_ingredients_by_recipe,
     update_recipe_title,  update_recipe_instructions, delete_ingredient
   
  
)

@index_views.route('/', methods=['GET'])
@jwt_required(optional=True)
def index_page():
    user = current_user if current_user else None
    is_authenticated = user is not None
<<<<<<< HEAD
    recipes = get_all_recipes()
    print("Recipes from DB1:", [r.title for r in recipes])
    recipes_json = [r.get_json() for r in recipes]
    return render_template(
        'index.html',
        current_user=user,
        is_authenticated=is_authenticated,
        recipes=recipes,
        recipes_json = recipes_json
        , num_ingredients = 1
=======
    return render_template(
        'index.html',
        current_user=user,
        is_authenticated=is_authenticated
>>>>>>> 2f67087418dbf7099b8153d59d01a86a0b869aac
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
    image = request.form.get('image')
    instructions = request.form.get('instructions')
    num_ingredients = int(request.form.get('num_ingredients', 1))

    if not title or not instructions:
        flash("Title and instructions are required.", "error")
        return redirect(url_for('index_views.index_page'))

    # Create the recipe
    recipe = create_recipe({
        'title': title,
        'image': image,
        'instructions': instructions,
        'user_id': current_user.id
    })

    # Add ingredients
    for i in range(num_ingredients):
        name = request.form.get(f'ingredient_name_{i}')
        quantity = request.form.get(f'ingredient_quantity_{i}')
        ing_image = request.form.get(f'ingredient_image_{i}')

        if name and quantity:
            add_ingredient_to_recipe({
                'recipe_id': recipe.id,
                'name': name,
                'quantity': quantity,
                'image': ing_image or ""
            })

    return redirect(url_for('index_views.index_page'))




@index_views.route('/updateRecipe/<int:id>', methods=['GET'])
@jwt_required()
def show_update_form(id):
    recipe = get_recipe(id)

    if not recipe or recipe.user_id != current_user.id:
        return redirect(url_for('index_views.index_page'))

    return render_template(
        'index.html',
        recipe_to_edit=recipe,
        recipes=get_all_recipes(),
        is_authenticated=True,
        current_user=current_user,
        num_ingredients=len(get_ingredients_by_recipe(id)),  # Show all ingredients
        ingredients_to_edit=get_ingredients_by_recipe(id)    # Pass them into Jinja
    )


@index_views.route('/updateRecipe/<int:id>', methods=['POST'])
@jwt_required()
def update_recipe(id):
    recipe = get_recipe(id)

    if not recipe or recipe.user_id != current_user.id:
        return redirect(url_for('index_views.index_page'))

    new_title = request.form.get('title')
    new_instructions = request.form.get('instructions')

    if not new_title or not new_instructions:
        return redirect(url_for('index_views.show_update_form', id=id))

    update_recipe_title(recipe.id, new_title)
    update_recipe_instructions(recipe.id, new_instructions)

    # Optional: handle updated ingredients here if needed

    return redirect(url_for('index_views.index_page'))


# Add ingredient to a specific recipe
@index_views.route('/addRecipeIngredient', methods=['POST'])
@jwt_required()
def add_recipe_ingredient_route():
    data = request.json
    recipe_id = data.get('recipe_id')
    name = data.get('name')
    image = data.get('image', '')
    quantity = data.get('quantity')
    if recipe_id and name and quantity:
        result = add_ingredient_to_recipe(recipe_id, name, image, quantity)
        return jsonify(result.get_json())
    return jsonify({'error': 'Missing fields'}), 400

# Delete ingredient from a specific recipe
@index_views.route('/deleteRecipeIngredient/<int:ingredient_id>', methods=['POST', 'DELETE'])
@jwt_required()
def delete_recipe_ingredient_route(ingredient_id):
    success = delete_ingredient(ingredient_id)
    if success:
        return redirect(request.referrer or url_for('index_views.index_page'))
    return jsonify({'error': 'Not found'}), 404





