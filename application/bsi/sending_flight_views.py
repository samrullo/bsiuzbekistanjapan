from application import db
from flask import render_template, redirect, flash
from application.utils.custom_url_for import url_for
from application.bsi import bsi_bp
from .models import SendingDate
from flask_login import login_required
from application.auth.permission_required import confirm_required, moderator_required
from .forms import SendingDateForm
from flask_babel import lazy_gettext as _


@bsi_bp.route("/<lang>/sending_dates")
@login_required
@confirm_required
@moderator_required
def sending_dates():
    sending_dates = SendingDate.query.all()
    return render_template("sending_dates.html",
                           page_header_title=_("Sending dates"),
                           sending_dates=sending_dates)


@bsi_bp.route("/<lang>/add_sending_date", methods=['GET', 'POST'])
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
@login_required
@confirm_required
@moderator_required
def remove_sending_date(sending_date_id):
    sending_date_record = SendingDate.query.get(sending_date_id)
    db.session.delete(sending_date_record)
    db.session.commit()
    flash(_("Successfully removed sending date %(sending_date)s", sending_date=sending_date_record.sending_date),
          "success")
    return redirect(url_for('bsi_bp.sending_dates'))
