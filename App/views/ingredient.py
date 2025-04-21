from flask import Blueprint, flash, redirect, render_template, request, send_from_directory, jsonify, url_for

from flask_jwt_extended import jwt_required, current_user
ingredient_views = Blueprint('ingredient_views', __name__, template_folder='../templates')

from App.controllers import (
     get_ingredients_by_user, update_user_ingredient,
     create_ingredient,  get_user_ingredient,  delete_user_ingredient
)
