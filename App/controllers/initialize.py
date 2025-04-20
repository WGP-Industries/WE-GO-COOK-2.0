from .user import create_user
from .recipe import create_recipe
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_user('joe', 'joepass')

    create_recipe(
    title='Chicken Alfredo',
    instructions='Cook pasta. Sauté chicken in butter. Add cream and parmesan. Combine with pasta.',
    user_id=1,
    image='https://www.themealdb.com/images/media/meals/syqypv1486981727.jpg'
)