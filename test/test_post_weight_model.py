import unittest
from base_test_class import BaseTestCase
from application import db
from application.auth.models import User
from application.post_weight.models import Country
from application.post_weight.models import PostWeight
from application.post_weight.models import generate_human_readable_post_weight_id
import datetime
from application.utils.date_utils import to_yyyymmdd


class PostWeightModelTestCase(BaseTestCase):
    def test_set_human_readable_post_weight_id(self):
        user = User(email="bsiuzbekistanjapanpost@gmail.com", name="BSI Uzbekistan")
        user.set_username()
        Country.insert_countries()
        sent_date = datetime.date(2020, 10, 19)
        post_weight = PostWeight(sent_date=sent_date, weight=13)
        post_weight.from_country = Country.query.filter_by(country_code="JP").first()
        post_weight.to_country = Country.query.filter_by(country_code="UZ").first()
        post_weight.user = user
        db.session.add(post_weight)
        db.session.commit()
        post_weight.human_readable_id = generate_human_readable_post_weight_id(post_weight)
        db.session.add(post_weight)
        db.session.commit()
        self.app.logger.info(f"first post weight human readable id : {post_weight.human_readable_id}")
        post_weights = PostWeight.query.filter(PostWeight.user_id == post_weight.user_id).filter(
            PostWeight.sent_date == post_weight.sent_date).all()
        self.assertEqual(post_weight.human_readable_id,
                         f"{post_weight.from_country.country_code}|{post_weight.to_country.country_code}|{post_weight.user.username}|{to_yyyymmdd(post_weight.sent_date)}|{post_weight.id}|{len(post_weights)}")
        post_weight_two = PostWeight(sent_date=sent_date, weight=14)
        post_weight_two.from_country = Country.query.filter_by(country_code="JP").first()
        post_weight_two.to_country = Country.query.filter_by(country_code="UZ").first()
        post_weight_two.user = user
        db.session.add(post_weight_two)
        db.session.commit()
        post_weight_two.human_readable_id = generate_human_readable_post_weight_id(post_weight_two)
        db.session.add(post_weight_two)
        db.session.commit()
        self.app.logger.info(f"second post weight human readable id : {post_weight_two.human_readable_id}")
        post_weights = PostWeight.query.filter(PostWeight.user_id == post_weight.user_id).filter(
            PostWeight.sent_date == post_weight.sent_date).all()
        self.assertEqual(post_weight_two.human_readable_id,
                         f"{post_weight_two.from_country.country_code}|{post_weight_two.to_country.country_code}|{post_weight_two.user.username}|{to_yyyymmdd(post_weight_two.sent_date)}|{post_weight_two.id}|{len(post_weights)}")

        # let's check the case when we update the post weight, most probably its sent date
        increment_part = post_weight_two.human_readable_id.split("|")[-1]
        post_weight_two.sent_date = datetime.date(2020, 10, 20)
        db.session.add(post_weight_two)
        db.session.commit()
        post_weight_two.human_readable_id = generate_human_readable_post_weight_id(post_weight_two)
        db.session.add(post_weight_two)
        db.session.commit()
        self.app.logger.info(
            f"second post weight human readable id after updating sent date : {post_weight_two.human_readable_id}")
        self.assertEqual(post_weight_two.human_readable_id,f"{post_weight_two.from_country.country_code}|{post_weight_two.to_country.country_code}|{post_weight_two.user.username}|{to_yyyymmdd(post_weight_two.sent_date)}|{post_weight_two.id}|{increment_part}")


if __name__ == '__main__':
    unittest.main()
