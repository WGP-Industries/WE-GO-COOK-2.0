from App.database import db


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(20))  # e.g., "2 cups", "1 tbsp"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity
        }

