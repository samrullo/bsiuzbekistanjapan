from application import db
import datetime
from flask_babel import lazy_gettext as _
from application.post_weight.models import Country


class BSIPostWeight(db.Model):
    __tablename__ = "bsi_post_weights"
    id = db.Column(db.Integer, primary_key=True)
    post_weight_id = db.Column(db.Integer, db.ForeignKey("post_weights.id"))
    post_weight = db.relationship("PostWeight", foreign_keys=[post_weight_id])
    weight = db.Column(db.Float)
    payment_amount = db.Column(db.Float)
    entered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    entered_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    modified_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    entered_by = db.relationship("User", foreign_keys=[entered_by_id])
    modified_by = db.relationship("User", foreign_keys=[modified_by_id])


class PostFlightStatus:
    FULL_FREE = 0
    FREE = 1
    MODERATELY_FREE = 2
    NOSPACELEFT = 3

    status_descriptions = {FULL_FREE: _('◎ ... fully available')}


class PostFlight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sending_date = db.Column(db.Date, unique=True)
    from_country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    to_country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    from_country = db.relationship("Country", foreign_keys=[from_country_id])
    to_country = db.relationship("Country", foreign_keys=[to_country_id])
    note = db.Column(db.String(100))
