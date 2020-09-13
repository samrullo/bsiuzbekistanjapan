from application import db
import datetime

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
