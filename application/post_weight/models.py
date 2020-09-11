from application import db
import datetime

class PostWeight(db.Model):
    __tablename__ = "post_weights"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    sent_date = db.Column(db.Date)
    weight = db.Column(db.Float)
    payment_amount = db.Column(db.Float)
    entered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_paid = db.Column(db.Boolean,default=False)
    is_removable = db.Column(db.Boolean,default=True)
    bsi_post_weight = db.relationship("BSIPostWeight", backref="user_post_weight")

    def update_modified_on(self):
        self.modified_on = datetime.datetime.utcnow()


class BSIPostWeight(db.Model):
    __tablename__ = "bsi_post_weights"
    id = db.Column(db.Integer, primary_key=True)
    post_weight_id = db.Column(db.Integer, db.ForeignKey("post_weights.id"))
    weight = db.Column(db.Float)
    payment_amount = db.Column(db.Float)
    entered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def update_modified_on(self):
        self.modified_on = datetime.datetime.utcnow()
