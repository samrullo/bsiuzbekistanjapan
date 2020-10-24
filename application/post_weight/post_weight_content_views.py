import datetime
from application import db
import pandas as pd
from flask import render_template, redirect, flash, current_app, request
from flask_login import login_required, current_user
from application.auth.permission_required import confirm_required
from application.utils.custom_url_for import url_for
from flask_babel import lazy_gettext as _
from . import post_weight_bp
from .models import PostWeight, PostWeightContent
from .models import generate_human_readable_post_weight_id
from .models import Country
from .forms import PostWeightContentForm
from application.post_weight.post_weight_utils import get_price_per_kg
from application import images
from application.utils.image_s3_upload import S3Uploader


@post_weight_bp.route("/<lang>/view_post_weight_content/<post_weight_content_id>")
def view_post_weight_content(post_weight_content_id):
    post_weight_content = PostWeightContent.query.get(post_weight_content_id)
    return render_template("single_post_weight_content.html",
                           page_header_title=_("Post weight content %(name)s", name=post_weight_content.name),
                           post_weight_content=post_weight_content)


@post_weight_bp.route("/<lang>/view_post_weight_contents/<post_weight_id>")
@login_required
@confirm_required
def view_post_weight_contents(post_weight_id):
    post_weight_contents = PostWeightContent.query.filter_by(post_weight_id=post_weight_id).all()
    post_weight_content_sums = [post_weight_content.price * post_weight_content.quantity for post_weight_content in
                                post_weight_contents]
    post_weight_content_sum = sum(post_weight_content_sums)
    post_weight = PostWeight.query.get(post_weight_id)
    return render_template("post_weight_contents.html",
                           page_header_title=_("Post weight content for the post %(post_id)s",
                                               post_id=post_weight.human_readable_id),
                           post_weight=post_weight,
                           post_weight_contents=post_weight_contents,
                           post_weight_content_sum=post_weight_content_sum)


@post_weight_bp.route("/<lang>/new_post_weight_content/<post_weight_id>", methods=['GET', 'POST'])
@login_required
@confirm_required
def new_post_weight_content(post_weight_id):
    post_weight = PostWeight.query.get(post_weight_id)
    form = PostWeightContentForm()
    if form.validate_on_submit():
        post_weight_content = PostWeightContent(post_weight_id=post_weight_id,
                                                name=form.name.data,
                                                price=form.price.data,
                                                quantity=form.quantity.data)

        db.session.add(post_weight_content)
        db.session.commit()

        # save post item image to s3 bucket if user specified the image
        if form.content_image.data:
            s3uploader = S3Uploader()
            content_image_filename = f"{post_weight_content.id}_{post_weight_content.name}"
            content_image_url = s3uploader.upload_photo_to_s3_bucket(form.content_image.data, content_image_filename,
                                                                     "post_item_images")
            post_weight_content.content_image_url = content_image_url
            db.session.add(post_weight_content)
            db.session.commit()

        # set post weight is_removable to False
        post_weight = PostWeight.query.get(post_weight_content.post_weight_id)
        post_weight.is_removable = False
        db.session.add(post_weight)
        db.session.commit()
        flash(_("Successfully added post weight content %(name)s | %(price)d | %(quantity)d",
                name=post_weight_content.name,
                price=post_weight_content.price,
                quantity=post_weight_content.quantity), "success")
        return redirect(url_for("post_weight_bp.view_post_weight_contents", post_weight_id=post_weight_id))
    return render_template("common_form_render.html", page_header_title=_("Add new post weight content for %(post_id)s",
                                                                          post_id=post_weight.human_readable_id),
                           form=form)


@post_weight_bp.route("/<lang>/edit_post_weight_content/<post_weight_content_id>", methods=['GET', 'POST'])
@login_required
@confirm_required
def edit_post_weight_content(post_weight_content_id):
    post_weight_content = PostWeightContent.query.get(post_weight_content_id)
    form = PostWeightContentForm()
    if form.validate_on_submit():
        post_weight_content.name = form.name.data
        post_weight_content.price = form.price.data
        post_weight_content.quantity = form.quantity.data
        post_weight_content.modified_on = datetime.datetime.utcnow()
        db.session.add(post_weight_content)
        db.session.commit()

        # save post item image to s3 bucket if user specified the image
        if form.content_image.data:
            s3uploader = S3Uploader()
            content_image_filename = f"{post_weight_content.id}_{post_weight_content.name}"
            content_image_url = s3uploader.upload_photo_to_s3_bucket(form.content_image.data, content_image_filename,
                                                                     "post_item_images")
            post_weight_content.content_image_url = content_image_url
            db.session.add(post_weight_content)
            db.session.commit()

        flash(_("Successfully updated post weight content %(name)s | %(price)d | %(quantity)d",
                name=post_weight_content.name,
                price=post_weight_content.price,
                quantity=post_weight_content.quantity), "success")
        return redirect(
            url_for("post_weight_bp.view_post_weight_contents", post_weight_id=post_weight_content.post_weight_id))
    form.name.data = post_weight_content.name
    form.price.data = post_weight_content.price
    form.quantity.data = post_weight_content.quantity
    return render_template("common_form_render.html", page_header_title=_("Edit post weight content for %(post_id)s",
                                                                          post_id=post_weight_content.post_weight.human_readable_id),
                           form=form)


@post_weight_bp.route("/<lang>/remove_post_weight_content/<post_weight_content_id>")
@login_required
@confirm_required
def remove_post_weight_content(post_weight_content_id):
    post_weight_content = PostWeightContent.query.get(post_weight_content_id)
    db.session.delete(post_weight_content)
    db.session.commit()
    post_weight_contents = PostWeightContent.query.filter_by(post_weight_id=post_weight_content.post_weight_id).all()
    if len(post_weight_contents) == 0:
        # set post weight is_removable to False
        post_weight = PostWeight.query.get(post_weight_content.post_weight_id)
        post_weight.is_removable = True
        db.session.add(post_weight)
        db.session.commit()
    flash(_("Successfully removed post weight content %(name)s | %(price)d | %(quantity)d",
            name=post_weight_content.name,
            price=post_weight_content.price,
            quantity=post_weight_content.quantity), "success")
    return redirect(
        url_for("post_weight_bp.view_post_weight_contents", post_weight_id=post_weight_content.post_weight_id))
