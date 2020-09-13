from application.main.models import BusinessGlobalVariable


def get_price_per_kg():
    price_per_kg_obj = BusinessGlobalVariable.query.filter_by(name='post_price_per_kg').first()
    if not price_per_kg_obj:
        BusinessGlobalVariable.insert_global_variables()
        price_per_kg_obj = BusinessGlobalVariable.query.filter_by(name='post_price_per_kg').first()
    return price_per_kg_obj.value
