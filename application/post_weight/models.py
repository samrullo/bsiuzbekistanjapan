from application import db
import datetime
from application.utils.date_utils import to_yyyymmdd


class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    country_code = db.Column(db.String(10))
    country_name = db.Column(db.String(100))

    @staticmethod
    def insert_countries(self):
        """
        Insert JP and UZ countries if not exists
        """
        countries = [('JP', 'Japan'), ('UZ', 'Uzbekistan')]
        for country_code, country_name in countries:
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

    def update_modified_on(self):
        self.modified_on = datetime.datetime.utcnow()

    def set_human_readable_post_weight_id(self):
        """
            <FROM><TO><USERNAME><USER ID><DATE><INCREMENTAL NUMBER>
        """
        post_weights = PostWeight.query.filter(PostWeight.user_id == self.user_id).filter(
            PostWeight.sent_date == self.sent_date).all()
        if not self.human_readable_id:
            self.human_readable_id = f"{self.from_country.country_code}|{self.to_country.country_code}|{self.user.username}|{to_yyyymmdd(self.sent_date)}|{len(post_weights) + 1}"
        else:
            increment_part = self.human_readable_id.split("|")[-1]
            self.human_readable_id = f"{self.from_country.country_code}|{self.to_country.country_code}|{self.user.username}|{to_yyyymmdd(self.sent_date)}|{increment_part}"

    def __repr__(self):
        return f"<ID:{self.id}, sent_date: {self.sent_date}, weight: {self.weight}, payment_amount: {self.payment_amount}>"

    def __str__(self):
        return f"<ID:{self.id}, sent_date: {self.sent_date}, weight: {self.weight}, payment_amount: {self.payment_amount}>"


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

    def __repr__(self):
        return f"<Name:{self.name}, email: {self.email}, phone: {self.phone}, telegram_username: {self.telegram_username}>"
