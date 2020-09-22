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
    is_paid = db.Column(db.Boolean, default=False)
    is_removable = db.Column(db.Boolean, default=True)
    bsi_post_weight = db.relationship("BSIPostWeight", backref="post_weight", uselist=False)

    def update_modified_on(self):
        self.modified_on = datetime.datetime.utcnow()

    def __repr__(self):
        return f"<ID:{self.id}, sent_date: {self.sent_date}, weight: {self.weight}, payment_amount: {self.payment_amount}>"

    def __str__(self):
        return f"<ID:{self.id}, sent_date: {self.sent_date}, weight: {self.weight}, payment_amount: {self.payment_amount}>"
