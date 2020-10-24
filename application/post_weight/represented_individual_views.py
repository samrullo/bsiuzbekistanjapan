import datetime
from application import db
from flask import render_template, redirect, flash, current_app
from application.utils.custom_url_for import url_for
from flask_babel import lazy_gettext as _
from application.post_weight import post_weight_bp
from flask_login import login_required, current_user

# import models and forms related to represented_individuals and recipients
from .models import RepresentedIndividual, Recipient
from application.post_weight.forms import RepresentedIndividualRecipientForm


# views to add, edit, view represented individuals
@post_weight_bp.route("/<lang>/view_represented_individuals")
def view_represented_individuals():
    return render_template("represented_individuals.html", page_header_title=_("Represented individuals"),
                           represented_individuals=current_user.represented_individuals)


@post_weight_bp.route("/<lang>/add_represented_individual", methods=['GET', 'POST'])
def add_represented_individual():
    form = RepresentedIndividualRecipientForm()
    if form.validate_on_submit():
        represented_individual = RepresentedIndividual(name=form.name.data,
                                                       email=form.email.data,
                                                       phone=form.phone.data,
                                                       telegram_username=form.telegram_username.data,
                                                       address=form.address.data,
                                                       )
        represented_individual.user = current_user
        db.session.add(represented_individual)
        db.session.commit()
        flash(_("Successfully added represented individual %(name)s", name=represented_individual.name), "success")
        return redirect(url_for("post_weight_bp.view_represented_individuals"))
    return render_template("common_form_render.html", page_header_title=_("Add represented individual"), form=form)


@post_weight_bp.route("/<lang>/edit_represented_individual/<represented_individual_id>", methods=['GET', 'POST'])
def edit_represented_individual(represented_individual_id):
    represented_individual = RepresentedIndividual.query.get(represented_individual_id)
    form = RepresentedIndividualRecipientForm()
    if form.validate_on_submit():
        represented_individual.name = form.name.data
        represented_individual.email = form.email.data
        represented_individual.phone = form.phone.data
        represented_individual.telegram_username = form.telegram_username.data
        represented_individual.address = form.address.data
        represented_individual.modified_on = datetime.datetime.utcnow()
        db.session.add(represented_individual)
        db.session.commit()
        flash(_("Successfully updated represented individual %(name)s", name=represented_individual.name), "success")
        return redirect(url_for("post_weight_bp.view_represented_individuals"))
    form.name.data = represented_individual.name
    form.email.data = represented_individual.email
    form.phone.data = represented_individual.phone
    form.telegram_username.data = represented_individual.telegram_username
    form.address.data = represented_individual.address
    return render_template("common_form_render.html",
                           page_header_title=_("Edit represented individual %(name)s",
                                               name=represented_individual.name),
                           form=form)


@post_weight_bp.route("/<lang>/remove_represented_individual/<represented_individual_id>")
def remove_represented_individual(represented_individual_id):
    represented_individual = RepresentedIndividual.query.get(represented_individual_id)
    db.session.delete(represented_individual)
    db.session.commit()
    flash(_("Successfully removed represented individual %(name)s", name=represented_individual.name), "success")
    return redirect(url_for("post_weight_bp.represented_individuals"))
