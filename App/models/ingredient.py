from App.database import db

#I think we should use this to store user ingredients 
class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image =db.Column(db.String(100), nullable=False)

    unit = db.Column(db.String(20)) 
    quantity =  db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, image, quantity, user_id, unit):
        self.name = name
        self.image = image
        self.quantity = quantity
        self.user_id = user_id
        self.unit = unit

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit
        }

