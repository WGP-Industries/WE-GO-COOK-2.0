from App.database import db

# -- RecipeIngredient Model (many-to-many with quantities) --
class RecipeIngredients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    image =db.Column(db.String(100), nullable=False)

    quantity = db.Column(db.String(20))  # e.g., "3 eggs", "1 tbsp sugar"

    def get_json(self):
        return {
            'name': self.name,
            'quantity': self.quantity
        }
