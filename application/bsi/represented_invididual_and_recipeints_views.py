from flask import render_template, redirect, flash
from application.bsi import bsi_bp
from flask_babel import lazy_gettext as _
from application.post_weight.models import RepresentedIndividual, Recipient


@bsi_bp.route("/<lang>/view_represented_individual/<represented_individual_id>")
def view_represented_individual(represented_individual_id):
    represented_individual = RepresentedIndividual.query.get(represented_individual_id)
    return render_template("user_represented_individual.html",
                           page_header_title=_("Represented individual info"),
                           represented_individual=represented_individual)


@bsi_bp.route("/<lang>/view_recipient/<recipient_id>")
def view_recipient(recipient_id):
    recipient = Recipient.query.get(recipient_id)
    return render_template("user_recipient.html",
                           page_header_title=_("Recipient info"),
                           recipient=recipient)
