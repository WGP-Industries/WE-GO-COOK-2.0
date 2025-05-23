# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin
from .ingredient import ingredient_views
from .missing_ingredients import missing_ingredients_views


views = [user_views, index_views, auth_views, ingredient_views, missing_ingredients_views] 
# blueprints must be added to this list
