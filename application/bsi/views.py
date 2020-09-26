from application import db
from flask import render_template, redirect, flash
from application.utils.custom_url_for import url_for
from flask_login import current_user
import datetime
from application import moment
from application.bsi import bsi_bp
from application.post_weight.post_weight_utils import get_price_per_kg
from application.post_weight.models import PostWeight
from .models import BSIPostWeight, SendingDate
from application.auth.models import User
from flask_login import login_required
from application.auth.permission_required import confirm_required, moderator_required
from .forms import BSIPostWeightForm, SendingDateForm
from flask_babel import lazy_gettext as _
import pandas as pd


@bsi_bp.route("/<lang>/moderator")
@login_required
@confirm_required
@moderator_required
def moderator():
    return render_template("bsi_moderator_home.html", page_header_title=_("Moderator menu"))


@bsi_bp.route("/<lang>/user_total_weights")
@login_required
@confirm_required
@moderator_required
def user_total_weights():
    users = User.query.all()
    users_with_total_weight = []
    for user in users:
        total_post_weight = sum([post_weight.weight for post_weight in user.post_weights])
        users_with_total_weight.append((user, total_post_weight))
    return render_template("bsi_user_total_weights.html",
                           page_header_title=_("User total weights"),
                           page_for_viewing_unpaid=False,
                           users_with_total_weight=users_with_total_weight)


@bsi_bp.route("/<lang>/unpaid_user_total_weights")
@login_required
@confirm_required
@moderator_required
def unpaid_user_total_weights():
    users = User.query.all()
    users_with_total_weight = []
    for user in users:
        total_post_weight = sum([post_weight.weight for post_weight in user.post_weights if not post_weight.is_paid])
        users_with_total_weight.append((user, total_post_weight))
    return render_template("bsi_user_total_weights.html",
                           page_header_title=_("Unpaid user total weights"),
                           page_for_viewing_unpaid=True,
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
    return render_template("bsi_weights_by_user.html",
                           page_header_title=_("Weights by user %(name)s", name=user.name),
                           page_for_viewing_unpaid=False,
                           user=user,
                           post_weights_grp_df=post_weights_grp_df)


@bsi_bp.route("/<lang>/unpaid_weights_by_user/<user_id>")
@login_required
@confirm_required
@moderator_required
def unpaid_weights_by_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    post_weights = PostWeight.query.filter(PostWeight.user_id == user.id).filter(PostWeight.is_paid == False).all()
    post_weight_list = [(post_weight.sent_date, post_weight.weight, post_weight.payment_amount) for post_weight in
                        post_weights]
    post_weights_df = pd.DataFrame(columns=['sent_date', 'weight', 'payment_amount'], data=post_weight_list)
    post_weights_grp_df = post_weights_df.groupby('sent_date').sum()
    return render_template("bsi_weights_by_user.html",
                           page_header_title=_("Unpaid weights by user %(name)s", name=user.name),
                           page_for_viewing_unpaid=True,
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
                           page_for_viewing_unpaid=False,
                           user=user,
                           post_weights=post_weights)


@bsi_bp.route("/<lang>/unpaid_weights_by_user_as_of_date/<user_id>/<adate>")
@login_required
@confirm_required
@moderator_required
def unpaid_weights_by_user_as_of_date(user_id, adate):
    user = User.query.filter_by(id=user_id).first()
    post_weights = PostWeight.query.filter(PostWeight.user_id == user_id).filter(PostWeight.sent_date == adate).filter(
        PostWeight.is_paid == False).all()
    return render_template("bsi_weights_by_user_as_of_date.html",
                           page_header_title=_("Unpaid post weights sent by %(name)s on %(date)s", name=user.name,
                                               date=adate),
                           page_for_viewing_unpaid=True,
                           user=user,
                           post_weights=post_weights)


@bsi_bp.route("/<lang>/add_bsi_weight/<post_weight_id>", methods=['GET', 'POST'])
@login_required
@confirm_required
@moderator_required
def add_bsi_weight(post_weight_id):
    form = BSIPostWeightForm()
    post_weight = PostWeight.query.get(post_weight_id)
    if form.validate_on_submit():
        bsi_post_weight = BSIPostWeight(post_weight_id=post_weight_id, weight=form.weight.data, entered_by=current_user,
                                        modified_by=current_user)
        price_per_kg = get_price_per_kg()
        bsi_post_weight.payment_amount = price_per_kg * bsi_post_weight.weight
        db.session.add(bsi_post_weight)
        db.session.commit()
        post_weight.is_removable = False
        db.session.add(post_weight)
        db.session.commit()
        flash(_("Successfully saved bsi post weight of %(weight)d kg sent on %(sent_date)s", weight=bsi_post_weight.weight,sent_date=bsi_post_weight.post_weight.sent_date), "success")
        return redirect(url_for('bsi_bp.weights_by_user_as_of_date', user_id=bsi_post_weight.post_weight.user.id,
                                adate=bsi_post_weight.post_weight.sent_date))
    return render_template("bsi_add_weight.html",
                           page_header_title=_("Add BSI weight"),
                           form=form,
                           post_weight=post_weight)


@bsi_bp.route("/<lang>/edit_bsi_weight/<bsi_post_weight_id>", methods=['GET', 'POST'])
@login_required
@confirm_required
@moderator_required
def edit_bsi_weight(bsi_post_weight_id):
    form = BSIPostWeightForm()
    bsi_post_weight = BSIPostWeight.query.get(bsi_post_weight_id)
    if form.validate_on_submit():
        bsi_post_weight.weight = form.weight.data
        bsi_post_weight.modified_on = datetime.datetime.utcnow()
        bsi_post_weight.modified_by = current_user
        db.session.add(bsi_post_weight)
        db.session.commit()
        flash(_("Successfully saved bsi post weight of %(weight)d kg sent on %(sent_date)s", weight=bsi_post_weight.weight,sent_date=bsi_post_weight.post_weight.sent_date), "success")
        return redirect(url_for('bsi_bp.weights_by_user_as_of_date', user_id=bsi_post_weight.post_weight.user.id,
                                adate=bsi_post_weight.post_weight.sent_date))
    form.weight.data = bsi_post_weight.weight
    return render_template("bsi_edit_weight.html",
                           page_header_title=_("Edit BSI post weight"),
                           form=form,
                           post_weight=bsi_post_weight.post_weight)


@bsi_bp.route("/<lang>/remove_bsi_weight/<bsi_post_weight_id>", methods=['GET', 'POST'])
@login_required
@confirm_required
@moderator_required
def remove_bsi_weight(bsi_post_weight_id):
    bsi_post_weight = BSIPostWeight.query.get(bsi_post_weight_id)
    db.session.delete(bsi_post_weight)
    db.session.commit()
    flash(_("Successfully removed bsi post weight %(bsi_post_weight)d kg sent on %(sent_date)s", bsi_post_weight=bsi_post_weight,sent_date=bsi_post_weight.post_weight.sent_date), "success")
    return redirect(url_for('bsi_bp.weights_by_user_as_of_date', user_id=bsi_post_weight.post_weight.user.id,
                            adate=bsi_post_weight.post_weight.sent_date))


@bsi_bp.route("/<lang>/mark_post_weight_as_paid_or_unpaid/<post_weight_id>")
@login_required
@confirm_required
@moderator_required
def mark_post_weight_as_paid_or_unpaid(post_weight_id):
    post_weight = PostWeight.query.get(post_weight_id)
    post_weight.is_paid = not post_weight.is_paid
    if post_weight.is_paid:
        post_weight.is_removable = False
        post_weight.is_editable = False
    else:
        post_weight.is_removable = True
        post_weight.is_editable = True
    db.session.add(post_weight)
    db.session.commit()
    flash(_("Marked post weight %(weight)d kg sent on %(sent_date)s as paid",weight=post_weight.weight,sent_date=post_weight.sent_date), "success")
    return redirect(url_for('bsi_bp.weights_by_user_as_of_date', user_id=post_weight.user.id,
                            adate=post_weight.sent_date))


@bsi_bp.route("/<lang>/view_user_profile/<user_id>")
@login_required
@confirm_required
@moderator_required
def view_user_profile(user_id):
    user = User.query.get(user_id)
    return render_template("bsi_user_profile.html",
                           page_header_title=_("%(name)s profile", name=user.name),
                           user=user)


@bsi_bp.route("/<lang>/sending_dates")
@login_required
@confirm_required
@moderator_required
def sending_dates():
    sending_dates = SendingDate.query.all()
    return render_template("sending_dates.html",
                           page_header_title=_("Sending dates"),
                           sending_dates=sending_dates)


@bsi_bp.route("/<lang>/add_sending_date",methods=['GET','POST'])
@login_required
@confirm_required
@moderator_required
def add_sending_date():
    form = SendingDateForm()
    if form.validate_on_submit():
        sending_date_record = SendingDate(sending_date=form.sending_date.data, note=form.note.data)
        db.session.add(sending_date_record)
        db.session.commit()
        flash(_("Successfully added sending date %(sending_date)s", sending_date=sending_date_record.sending_date),
              "success")
        return redirect(url_for('bsi_bp.moderator'))
    return render_template("add_sending_date.html",
                           page_header_title=_("Add sending date"),
                           form=form)


@bsi_bp.route("/<lang>/remove_sending_date/<sending_date_id>")
def remove_sending_date(sending_date_id):
    sending_date_record = SendingDate.query.get(sending_date_id)
    db.session.delete(sending_date_record)
    db.session.commit()
    flash(_("Successfully removed sending date %(sending_date)s", sending_date=sending_date_record.sending_date),
          "success")
    return redirect(url_for('bsi_bp.sending_dates'))
