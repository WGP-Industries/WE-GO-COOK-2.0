from App.database import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image =db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy=True)

    def get_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'instructions': self.instructions,
            'ingredients': [ri.get_json() for ri in self.ingredients]
        }