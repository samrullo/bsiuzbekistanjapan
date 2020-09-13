from flask import render_template, redirect
import datetime
from application.bsi import bsi_bp
from application.post_weight.post_weight_utils import get_price_per_kg
from application.auth.models import User
from application.post_weight.models import PostWeight
from .models import BSIPostWeight
from flask_login import login_required
from application.auth.permission_required import confirm_required, moderator_required
from .forms import BSIPostWeightForm
from flask_babel import lazy_gettext as _


@bsi_bp.route("/<lang>/weights_by_user/<user_id>")
@login_required
@confirm_required
@moderator_required
def weights_by_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template("bsi_weights_by_user.html", page_header_title=_("Weights by user %(name)s", name=user.name),
                           user=user)

@bsi_bp.route("/<lang>/weights_by_user_as_of_date/<user_id>/<adate>")
@login_required
@confirm_required
@moderator_required
def weights_by_user_as_of_date(user_id,adate):
    user=User.query.filter_by(id=user_id).first()
    post_weights=PostWeight.query.filter(user_id=user_id).filter(sent_date=adate).all()
    return render_template("bsi_weights_by_user_as_of_date.html",
                           page_header_title=_("Post weights sent by %(name)s on %(date)s",name=user.name,date=adate),
                           user=user,
                           post_weights=post_weights)

@bsi_bp.route("/<lang>/add_bsi_weight/<post_weight_id>")
@login_required
@confirm_required
@moderator_required
def add_bsi_weight(post_weight_id):
    form = BSIPostWeightForm()
    if form.validate_on_submit():
        bsi_post_weight = BSIPostWeight(post_weight_id=post_weight_id, weight=form.weight.data)
        price_per_kg = get_price_per_kg()
        bsi_post_weight.payment_amount = price_per_kg * bsi_post_weight.weight
        bsi_post_weight.entered_on = datetime.datetime.utcnow()
        bsi_post_weight.update_modified_on()
    post_weight = PostWeight.query.filter_by(id=post_weight_id).first()
    return render_template("bsi_add_weight.html", page_header_title=_("Add BSI weight"),
                           form=form,
                           post_weight=post_weight)

@bsi_bp.route("/<lang>/edit_bsi_weight/<bsi_post_weight_id>")
@login_required
@confirm_required
@moderator_required
def edit_bsi_weight(bsi_post_weight_id):
    form=BSIPostWeightForm()
    bsi_post_weight=BSIPostWeight.query.filter_by(id=bsi_post_weight_id).first()
    form.weight=bsi_post_weight.weight
    return render_template("")