from application import db
import pandas as pd
from flask import render_template, redirect, flash, current_app
from application.utils.custom_url_for import url_for
from flask_babel import lazy_gettext as _
from application.post_weight import post_weight_bp
from flask_login import login_required, current_user
from .models import PostWeight
from .forms import PostWeightForm
from application.post_weight.post_weight_utils import get_price_per_kg
from application.auth.permission_required import confirm_required


@post_weight_bp.route("/<lang>/post_weight_home")
@login_required
@confirm_required
def post_weight_home():
    return render_template("post_weight_home.html",
                           page_header_title=_("Post weights by %(name)s", name=current_user.name))


@post_weight_bp.route("/<lang>/post_weight_by_date")
@login_required
@confirm_required
def post_weights_by_date():
    post_weights = current_user.post_weights
    post_weight_list = [(post_weight.sent_date, post_weight.weight, post_weight.payment_amount) for post_weight in
                        post_weights]
    post_weights_df = pd.DataFrame(columns=['sent_date', 'weight', 'payment_amount'], data=post_weight_list)
    post_weights_grp_df = post_weights_df.groupby('sent_date').sum()
    return render_template("post_weights_by_date.html",
                           page_header_title=_("Post weights by %(name)s grouped by sent dates", name=current_user.name)
                           , post_weights_grp_df=post_weights_grp_df)


@post_weight_bp.route("/<lang>/post_weight_as_of_date/<adate>")
@login_required
@confirm_required
def post_weights_as_of_date(adate):
    post_weights = PostWeight.query.filter(PostWeight.user_id == current_user.id).filter(
        PostWeight.sent_date == adate).all()
    return render_template("post_weights_as_of_date.html",
                           page_header_title=_("Post weights sent by %(name)s on %(date)s", name=current_user.name,
                                               date=adate),
                           post_weights=post_weights)


@post_weight_bp.route("/<lang>/post_weights")
@login_required
@confirm_required
def post_weights():
    return render_template("all_post_weights.html",
                           page_header_title=_("All post weights sent by %(name)s", name=current_user.name),
                           all_post_weights=current_user.post_weights)


@post_weight_bp.route("/<lang>/unpaid_post_weights")
@login_required
@confirm_required
def unpaid_post_weights():
    unpaid_post_weights = PostWeight.query.filter(PostWeight.user_id==current_user.id).filter(PostWeight.is_paid==False).all()
    total_unpaid_weight=sum([post_weight.weight for post_weight in unpaid_post_weights])
    total_unpaid_amount=sum([post_weight.payment_amount for post_weight in unpaid_post_weights])
    summary={'total_unpaid_weight':total_unpaid_weight,'total_unpaid_amount':total_unpaid_amount}
    return render_template("unpaid_post_weights.html",
                           page_header_title=_("Unpaid post weights by %(name)s", name=current_user.name),
                           unpaid_post_weights=unpaid_post_weights,
                           summary=summary)


@post_weight_bp.route("/<lang>/new_post_weight", methods=['GET', 'POST'])
@login_required
@confirm_required
def new_post_weight():
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
    return render_template("new_weight.html", form=form, page_header_title=_("Enter new weight"))


@post_weight_bp.route("/<lang>/edit_post_weight/<post_weight_id>", methods=['GET', 'POST'])
@login_required
@confirm_required
def edit_post_weight(post_weight_id):
    post_weight = PostWeight.query.get(post_weight_id)
    form = PostWeightForm()
    if form.validate_on_submit():
        post_weight.weight = form.weight.data
        post_weight.sent_date = form.sent_date.data
        post_weight.payment_amount = post_weight.weight * get_price_per_kg()
        db.session.add(post_weight)
        db.session.commit()
        flash(_("Successfully updated post weight"), "success")
        return redirect(url_for("post_weight_bp.post_weights_as_of_date", adate=post_weight.sent_date))
    form.sent_date.data = post_weight.sent_date
    form.weight.data = post_weight.weight
    return render_template("edit_weight.html", page_header_title=_("Edit post weight"), form=form)

@post_weight_bp.route("/<lang>/remove_weight/<post_weight_id>",methods=['GET','POST'])
@login_required
@confirm_required
def remove_post_weight(post_weight_id):
    post_weight=PostWeight.query.get(post_weight_id)
    db.session.delete(post_weight)
    db.session.commit()
    flash(_("Successfully removed post weight"), "success")
    return redirect(url_for("post_weight_bp.post_weights_as_of_date",adate=post_weight.sent_date))