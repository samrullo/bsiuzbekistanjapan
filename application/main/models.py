from application import db


class BusinessGlobalVariable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(200))
    value = db.Column(db.Float)

    @staticmethod
    def insert_global_variables():
        global_business_variables=[('post_price_per_kg','Post price per kg',2000)]
        for global_business_variable in global_business_variables:
            gb_var=BusinessGlobalVariable.query.filter_by(name=global_business_variable[0]).first()
            if gb_var:
                gb_var.description=global_business_variable[1]
                gb_var.value=global_business_variable[2]
            else:
                gb_var=BusinessGlobalVariable(name=global_business_variable[0],description=global_business_variable[1],
                                              value=global_business_variable[2])
            db.session.add(gb_var)
        db.session.commit()
