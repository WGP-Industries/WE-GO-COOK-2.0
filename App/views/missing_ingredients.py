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

