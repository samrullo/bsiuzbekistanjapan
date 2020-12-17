from application import db
from flask import render_template, redirect, flash
from application.utils.custom_url_for import url_for
from flask import request
from flask_login import current_user
import datetime
from application import moment
from application.bsi import bsi_bp
from application.post_weight.post_weight_utils import get_price_per_kg
from application.post_weight.models import PostWeight
from application.post_weight.forms import PostTrackingStatusForm
from application.post_weight.models import PostTrackingStatus
from .models import BSIPostWeight, PostFlight
from application.auth.models import User
from flask_login import login_required
from application.auth.permission_required import confirm_required, moderator_required
from .forms import BSIPostWeightForm, SendingDateForm
from flask_babel import lazy_gettext as _
import pandas as pd


@bsi_bp.route("/<lang>/change_tracking_status/<post_weight_id>", methods=['GET', 'POST'])
def change_tracking_status(post_weight_id):
    post_weight = PostWeight.query.get(post_weight_id)
    form = PostTrackingStatusForm()
    if form.validate_on_submit():
        post_weight.tracking_status = form.tracking_status.data
        db.session.add(post_weight)
        db.session.commit()
        flash(_("Successfully updated tracking status to %(status)s", status=post_weight.tracking_status), "success")
        next = request.args.get('next')
        if next:
            return redirect(next)
        else:
            return redirect(url_for('bsi_bp.unpaid_weights_by_user_as_of_date', user_id=post_weight.user_id,
                                    adate=post_weight.sent_date))
    form.tracking_status.data = post_weight.tracking_status
    return render_template("common_form_render.html",
                           page_header_title=_("Change tracking status of %(post_id)s",
                                               post_id=post_weight.human_readable_id),
                           form=form)
