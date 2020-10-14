from . import gmailapi_bp
from flask import current_app, redirect, request, render_template, flash
from application.auth.permission_required import admin_required
from application.utils.custom_url_for import url_for
from .gmail_api_server_side_authorization import get_authorization_url
from .gmail_api_server_side_authorization import get_credentials
from .gmail_api_server_side_authorization import NoRefreshTokenException
from flask_babel import lazy_gettext as _
from .forms import GmailAPIForm
from .gmailapi_send_mail import send_mail


@gmailapi_bp.route("/<lang>/gmailapi")
def gmailapi():
    return render_template("gmailapi_main.html", page_header_title=_("Gmail API main page"))


@gmailapi_bp.route("/<lang>/gmail_login")
@admin_required
def gmail_login():
    authorization_url = get_authorization_url(current_app.config.get('MAIL_SENDER'), "")
    current_app.logger.info(f"authorization url : {authorization_url}")
    return redirect(authorization_url)


@gmailapi_bp.route("/<lang>/gmail_login/callback")
@admin_required
def callback():
    # Get authorization code Google sent back to you
    authorization_code = request.args.get("code")
    try:
        # although we don't use creds here, get_credentials function will store new credentials
        # with refresh token in the pickle file
        creds = get_credentials(authorization_code, "")
    except NoRefreshTokenException as error:
        current_app.logger.info(
            f"NoRefreshTokenException exceptions was raised. will redirect to {error.authorization_url}")
        return redirect(error.authorization_url)
    return redirect(url_for("gmailapi_bp.gmailapi"))


@gmailapi_bp.route("/<lang>/gmailapi_sendmail", methods=['GET', 'POST'])
@admin_required
def gmailapi_sendmail():
    form = GmailAPIForm()
    if form.validate_on_submit():
        send_mail(form.subject.data, current_app.config.get('MAIL_SENDER'), form.email.data, form.body.data,
                  form.body.data)
        flash(_("Successfully sent message"), "success")
        return redirect(url_for("gmailapi_bp.gmailapi"))
    return render_template("gmailapi_sendmail.html", page_header_title=_("Send test email"), form=form)
