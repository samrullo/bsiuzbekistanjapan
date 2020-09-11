from application import db
from flask import render_template, redirect, flash, current_app
from application.utils.custom_url_for import url_for
from flask_babel import lazy_gettext as _
from application.post_weight import post_weight_bp
from flask_login import login_required, current_user
from .models import PostWeight
from .forms import PostWeightForm
from application.post_weight.post_weight_utils import get_price_per_kg


@post_weight_bp.route("/<lang>/post_weights")
@login_required
def post_weights():
    all_post_weights=PostWeight.query.filter_by(user_id=current_user.id).all()
    return render_template("all_post_weights.html",
                           page_header_title=_("All post weights sent by %(name)s", name=current_user.name),
                           all_post_weights=all_post_weights)


@post_weight_bp.route("/<lang>/new_weight",methods=['GET','POST'])
@login_required
def new_weight():
    form = PostWeightForm()
    if form.validate_on_submit():
        new_weight = PostWeight(sent_date=form.sent_date.data, weight=form.weight.data)
        price_per_kg = get_price_per_kg()
        new_weight.payment_amount = new_weight.weight * price_per_kg
        new_weight.user = current_user
        db.session.add(new_weight)
        db.session.commit()
        flash(
            _("Successfully inserted new weight %(weight)s with paid amount %(paid_amount)s", weight=new_weight.weight,
              paid_amount=new_weight.payment_amount), "success")
        return redirect(url_for('post_weight_bp.post_weights'))
    return render_template("new_weight.html", form=form,page_header_title=_("Enter new weight"))
