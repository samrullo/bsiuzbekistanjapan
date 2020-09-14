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
    entered_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    modified_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    entered_by = db.relationship("User", foreign_keys=[entered_by_id])
    modified_by = db.relationship("User", foreign_keys=[modified_by_id])
