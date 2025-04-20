from App.database import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)

    ingredients = db.relationship('RecipeIngredients', backref='recipe', lazy=True)

    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # backref so you can do current_user.recipes
    user = db.relationship('User', back_populates='recipes')
    def __init__(self, title, image, instructions, user_id):
        self.title = title
        self.image = image
        self.instructions = instructions
        self.user_id = user_id

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image,
            'instructions': self.instructions,
            'ingredients': [ri.get_json() for ri in self.ingredients]
        }
