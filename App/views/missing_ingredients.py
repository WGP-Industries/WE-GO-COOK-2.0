from flask import Blueprint, flash, redirect, render_template, request, send_from_directory, jsonify, url_for

from flask_jwt_extended import jwt_required, current_user
missing_ingredients_views = Blueprint('missing_ingredients_views', __name__, template_folder='../templates')

from App.controllers import (
    create_user, initialize, get_all_recipes, get_ingredients_by_user, update_user_ingredient,
    create_recipe, create_ingredient, delete_recipe, get_ingredient,
    add_ingredient_to_recipe, get_all_recipes_json, get_recipes_by_user,get_recipe,  get_ingredients_by_recipe,
     update_recipe_title,  update_recipe_instructions, delete_ingredient, update_ingredient_image, 
     update_ingredient_name, update_ingredient_quantity, get_user_ingredient,  delete_user_ingredient, get_recipes_missing_ingredients
   
  
)

@missing_ingredients_views.route('/missing_ingredients', methods=['GET'])
@jwt_required()
def missing_ingredients_page():
    user = current_user
    is_authenticated = user is not None
    q = request.args.get("q", default='', type=str)
    sort_by = request.args.get("sort_by", default='title_asc')

    all_missing = get_recipes_missing_ingredients(user.id)

    
    if q:
        all_missing = [entry for entry in all_missing if q.lower() in entry["recipe"].title.lower()]

    if sort_by == "title_asc":
        all_missing.sort(key=lambda x: x["recipe"].title.lower())
    elif sort_by == "title_desc":
        all_missing.sort(key=lambda x: x["recipe"].title.lower(), reverse=True)
    elif sort_by == "id_asc":
        all_missing.sort(key=lambda x: x["recipe"].id)
    elif sort_by == "id_desc":
        all_missing.sort(key=lambda x: x["recipe"].id, reverse=True)

    return render_template(
        "missing_ingredients.html",
        current_user=user,
        is_authenticated=is_authenticated,
        recipes=all_missing,
        q=q,
        sort_by=sort_by,
        num_recipes=len(all_missing)
    )

