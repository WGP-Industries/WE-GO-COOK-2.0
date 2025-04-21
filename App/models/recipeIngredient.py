from App.database import db


#Recipe Model that hopefylly does what i need it to do
class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    image =db.Column(db.String(100), nullable=False) 
    unit = db.Column(db.String(20)) 
    quantity =  db.Column(db.Float, nullable=False)
   
    def __init__(self, recipe_id, name, image, quantity, unit):
        self.recipe_id = recipe_id
        self.name = name
        self.image = image
        self.quantity = quantity
        self.unit = unit
        


    def get_json(self):
        return {
            'name': self.name,
            'quantity': self.quantity,
            'unit':self.unit
        }
