from application.main.models import BusinessGlobalVariable
from .models import UserPostWeightPrice
from flask_login import current_user
import datetime


def get_price_per_kg():
    price_per_kg_obj = BusinessGlobalVariable.query.filter_by(name='post_price_per_kg').first()
    if not price_per_kg_obj:
        BusinessGlobalVariable.insert_global_variables()
        price_per_kg_obj = BusinessGlobalVariable.query.filter_by(name='post_price_per_kg').first()
    if current_user.is_authenticated and current_user.is_confirmed:
        user_post_weight_price = UserPostWeightPrice.query.filter(
            UserPostWeightPrice.user_id == current_user.id).filter(
            UserPostWeightPrice.from_date <= datetime.date.today()).filter(
            UserPostWeightPrice.to_date >= datetime.date.today()).first()
    else:
        user_post_weight_price = None
    if user_post_weight_price:
        price_per_kg = user_post_weight_price.post_weight_price
    else:
        price_per_kg = price_per_kg_obj.value
    return price_per_kg
