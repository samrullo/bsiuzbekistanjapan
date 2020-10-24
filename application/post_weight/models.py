from application import db
import datetime
from application.utils.date_utils import to_yyyymmdd
import logging


class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(10))
    country_name = db.Column(db.String(100))

    @staticmethod
    def insert_countries():
        """
        Insert JP and UZ countries if not exists
        """
        countries = [('JP', 'Japan'), ('UZ', 'Uzbekistan')]
        for country_code, country_name in countries:
            if not Country.query.filter_by(country_code=country_code).first():
                country = Country(country_code=country_code, country_name=country_name)
                db.session.add(country)
                db.session.commit()


class PostWeight(db.Model):
    __tablename__ = "post_weights"
    id = db.Column(db.Integer, primary_key=True)
    human_readable_id = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    sent_date = db.Column(db.Date)
    from_country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    to_country_id = db.Column(db.Integer, db.ForeignKey("countries.id"))
    from_country = db.relationship("Country", foreign_keys=[from_country_id])
    to_country = db.relationship("Country", foreign_keys=[to_country_id])
    represented_individual_id = db.Column(db.Integer, db.ForeignKey("represented_individuals.id"))
    recipient_id = db.Column(db.Integer, db.ForeignKey("recipients.id"))
    weight = db.Column(db.Float)
    payment_amount = db.Column(db.Float)
    entered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_paid = db.Column(db.Boolean, default=False)
    is_removable = db.Column(db.Boolean, default=True)
    is_editable = db.Column(db.Boolean, default=True)
    post_weight_contents = db.relationship("PostWeightContent", backref="post_weight", lazy="dynamic")

    def update_modified_on(self):
        self.modified_on = datetime.datetime.utcnow()

    def __repr__(self):
        return f"<ID:{self.id}, sent_date: {self.sent_date}, weight: {self.weight}, payment_amount: {self.payment_amount}>"

    def __str__(self):
        return f"<ID:{self.id}, sent_date: {self.sent_date}, weight: {self.weight}, payment_amount: {self.payment_amount}>"


def generate_human_readable_post_weight_id(post_weight):
    """
        <FROM><TO><USERNAME><USER ID><DATE><POST WEIGHT UNIQUE INTEGER ID><INCREMENTAL NUMBER>
    """
    post_weights = PostWeight.query.filter(PostWeight.user_id == post_weight.user_id).filter(
        PostWeight.sent_date == post_weight.sent_date).all()
    logging.debug(
        f"there are total of {len(post_weights)} with user {post_weight.user} and sent_date {post_weight.sent_date}")
    logging.debug(f"post weight human readable id before : {post_weight.human_readable_id}")
    if post_weight.human_readable_id is None:
        human_readable_id = f"{post_weight.from_country.country_code}|{post_weight.to_country.country_code}|{post_weight.user.username}|{to_yyyymmdd(post_weight.sent_date)}|{post_weight.id}|{len(post_weights)}"
        logging.debug(f"human readable id was None, after setting : {human_readable_id}")
    else:
        increment_part = post_weight.human_readable_id.split("|")[-1]
        human_readable_id = f"{post_weight.from_country.country_code}|{post_weight.to_country.country_code}|{post_weight.user.username}|{to_yyyymmdd(post_weight.sent_date)}|{post_weight.id}|{increment_part}"
        logging.debug(f"human readable id was not None, after setting : {human_readable_id}")
    return human_readable_id


class PostWeightContent(db.Model):
    __tablename__ = "post_weight_contents"
    id = db.Column(db.Integer, primary_key=True)
    post_weight_id = db.Column(db.Integer, db.ForeignKey("post_weights.id"), nullable=False)
    name = db.Column(db.String(250))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    extra_note = db.Column(db.String(250), nullable=True)
    content_image_url = db.Column(db.String(300))
    entered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class RepresentedIndividual(db.Model):
    __tablename__ = "represented_individuals"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(250), nullable=True)
    telegram_username = db.Column(db.String(250), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_weights = db.relationship("PostWeight", backref="represented_individual", lazy="dynamic")
    entered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Name:{self.name}, email: {self.email}, phone: {self.phone}, telegram_username: {self.telegram_username}>"


class Recipient(db.Model):
    __tablename__ = "recipients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(250), nullable=True)
    phone = db.Column(db.String(250), nullable=True)
    telegram_username = db.Column(db.String(250), nullable=True)
    address = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_weights = db.relationship("PostWeight", backref="recipient", lazy="dynamic")
    entered_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<Name:{self.name}, email: {self.email}, phone: {self.phone}, telegram_username: {self.telegram_username}>"
