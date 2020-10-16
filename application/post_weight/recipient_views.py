from application import db
from flask import render_template, redirect, flash, current_app
from application.utils.custom_url_for import url_for
from flask_babel import lazy_gettext as _
from application.post_weight import post_weight_bp
from flask_login import login_required, current_user

# import models and forms related to recipients and recipients
from .models import Recipient, Recipient
from application.post_weight.forms import RepresentedIndividualRecipientForm


# views to add, edit, view recipients
@post_weight_bp.route("/<lang>/view_recipients")
def view_recipients():
    return render_template("recipients.html", page_header_title=_("Recipients"),
                           recipients=current_user.recipients)


@post_weight_bp.route("/<lang>/add_recipient", methods=['GET', 'POST'])
def add_recipient():
    form = RepresentedIndividualRecipientForm()
    if form.validate_on_submit():
        recipient = Recipient(name=form.name.data,
                              email=form.email.data,
                              phone=form.phone.data,
                              telegram_username=form.telegram_username.data,
                              address=form.address.data)
        recipient.user = current_user
        db.session.add(recipient)
        db.session.commit()
        flash(_("Successfully added recipient %(name)s", name=recipient.name), "success")
        return redirect(url_for("post_weight_bp.view_recipients"))
    return render_template("common_form_render.html", page_header_title=_("Add recipient"), form=form)


@post_weight_bp.route("/<lang>/edit_recipient/<recipient_id>", methods=['GET', 'POST'])
def edit_recipient(recipient_id):
    recipient = Recipient.query.get(recipient_id)
    form = RepresentedIndividualRecipientForm()
    if form.validate_on_submit():
        recipient.name = form.name.data
        recipient.email = form.email.data
        recipient.phone = form.phone.data
        recipient.telegram_username = form.telegram_username.data
        recipient.address = form.address.data
        db.session.add(recipient)
        db.session.commit()
        flash(_("Successfully updated recipient %(name)s", name=recipient.name), "success")
        return redirect(url_for("post_weight_bp.view_recipients"))
    form.name.data = recipient.name
    form.email.data = recipient.email
    form.phone.data = recipient.phone
    form.telegram_username.data = recipient.telegram_username
    form.address.data = recipient.address
    return render_template("common_form_render.html",
                           page_header_title=_("Edit recipient %(name)s",
                                               name=recipient.name),
                           form=form)


@post_weight_bp.route("/<lang>/remove_recipient/<recipient_id>")
def remove_recipient(recipient_id):
    recipient = Recipient.query.get(recipient_id)
    db.session.delete(recipient)
    db.session.commit()
    flash(_("Successfully removed recipient %(name)s", name=recipient.name), "success")
    return redirect(url_for("post_weight_bp.recipients"))
