from application import db
from flask import render_template, redirect, flash
from application.utils.custom_url_for import url_for
from flask_login import current_user
import datetime
from application import moment
from application.bsi import bsi_bp
from application.post_weight.post_weight_utils import get_price_per_kg
from application.post_weight.models import PostWeight
from .models import BSIPostWeight
from application.auth.models import User
from flask_login import login_required
from application.auth.permission_required import confirm_required, moderator_required
from .forms import BSIPostWeightForm
from flask_babel import lazy_gettext as _
import pandas as pd


@bsi_bp.route("/<lang>/moderator")
@login_required
@confirm_required
@moderator_required
def moderator():
    users = User.query.all()
    users_with_total_weight = []
    for user in users:
        total_post_weight = sum([post_weight.weight for post_weight in user.post_weights])
        users_with_total_weight.append((user, total_post_weight))
    return render_template("bsi_moderator.html", page_header_title=_("User list for BSI moderator"),
                           users_with_total_weight=users_with_total_weight)


@bsi_bp.route("/<lang>/weights_by_user/<user_id>")
@login_required
@confirm_required
@moderator_required
def weights_by_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    post_weights = user.post_weights
    post_weight_list = [(post_weight.sent_date, post_weight.weight, post_weight.payment_amount) for post_weight in
                        post_weights]
    post_weights_df = pd.DataFrame(columns=['sent_date', 'weight', 'payment_amount'], data=post_weight_list)
    post_weights_grp_df = post_weights_df.groupby('sent_date').sum()
    return render_template("bsi_weights_by_user.html", page_header_title=_("Weights by user %(name)s", name=user.name),
                           user=user,
                           post_weights_grp_df=post_weights_grp_df)


@bsi_bp.route("/<lang>/weights_by_user_as_of_date/<user_id>/<adate>")
@login_required
@confirm_required
@moderator_required
def weights_by_user_as_of_date(user_id, adate):
    user = User.query.filter_by(id=user_id).first()
    post_weights = PostWeight.query.filter(PostWeight.user_id == user_id).filter(PostWeight.sent_date == adate).all()
    return render_template("bsi_weights_by_user_as_of_date.html",
                           page_header_title=_("Post weights sent by %(name)s on %(date)s", name=user.name, date=adate),
                           user=user,
                           post_weights=post_weights)


@bsi_bp.route("/<lang>/add_bsi_weight/<post_weight_id>", methods=['GET', 'POST'])
@login_required
@confirm_required
@moderator_required
def add_bsi_weight(post_weight_id):
    form = BSIPostWeightForm()
    if form.validate_on_submit():
        bsi_post_weight = BSIPostWeight(post_weight_id=post_weight_id, weight=form.weight.data, entered_by=current_user,
                                        modified_by=current_user)
        price_per_kg = get_price_per_kg()
        bsi_post_weight.payment_amount = price_per_kg * bsi_post_weight.weight
        db.session.add(bsi_post_weight)
        db.session.commit()
        flash(_("Successfully saved bsi post weight of %(weight)d", weight=bsi_post_weight.weight), "success")
        return redirect(url_for('bsi_bp.weights_by_user_as_of_date', user_id=bsi_post_weight.post_weight.user.id,
                                adate=bsi_post_weight.post_weight.sent_date))
    post_weight = PostWeight.query.filter_by(id=post_weight_id).first()
    return render_template("bsi_add_weight.html", page_header_title=_("Add BSI weight"),
                           form=form,
                           post_weight=post_weight)


@bsi_bp.route("/<lang>/edit_bsi_weight/<bsi_post_weight_id>", methods=['GET', 'POST'])
@login_required
@confirm_required
@moderator_required
def edit_bsi_weight(bsi_post_weight_id):
    form = BSIPostWeightForm()
    bsi_post_weight = BSIPostWeight.query.filter_by(id=bsi_post_weight_id).first()
    if form.validate_on_submit():
        bsi_post_weight.weight=form.weight.data
        bsi_post_weight.modified_on=datetime.datetime.utcnow()
        bsi_post_weight.modified_by=current_user
        db.session.add(bsi_post_weight)
        db.session.commit()
        flash(_("Successfully saved bsi post weight of %(weight)s", weight=bsi_post_weight.weight), "success")
        return redirect(url_for('bsi_bp.weights_by_user_as_of_date', user_id=bsi_post_weight.post_weight.user.id,
                                adate=bsi_post_weight.post_weight.sent_date))
    form.weight.data = bsi_post_weight.weight
    return render_template("bsi_edit_weight.html",
                           page_header_title=_("Edit BSI post weight"),
                           form=form,
                           post_weight=bsi_post_weight.post_weight)
