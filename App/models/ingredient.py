from App.database import db


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image =db.Column(db.String(100), nullable=False)

    quantity = db.Column(db.String(20))  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, name, image, quantity, user_id):
        self.name = name
        self.image = image
        self.quantity = quantity
        self.user_id = user_id

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity
        }

