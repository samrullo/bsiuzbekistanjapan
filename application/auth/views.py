import datetime
from application.auth import auth_bp
from flask import render_template, redirect, flash, request
from application.utils.custom_url_for import url_for
from flask_babel import lazy_gettext as _
from flask import current_app
from flask_login import login_required, logout_user, login_user
from .forms import LoginForm, RegisterForm, ResetPasswordSendLinkForm, ResetPasswordForm
from .models import User
from application import db
from itsdangerous import URLSafeSerializer
from flask_login import current_user
from application.utils.email_asynch import send_mail
from application.utils.token import generate_token, confirm_token, confirm_reset_password_token


@auth_bp.route("/<lang>/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data,is_google_account=False).first()
        if user and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main_bp.secret')
            return redirect(next)
        flash(_("Invalid email or password"), "danger")
    return render_template("login.html", form=form,page_header_title=_("Login"))


@auth_bp.route("/<lang>/logout")
@login_required
def logout():
    logout_user()
    flash(_("Logged you out"), "success")
    return redirect(url_for('main_bp.home'))


@auth_bp.route('/<lang>/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data, is_confirmed=False)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        token = generate_token(current_user.email)
        plain_text_body = render_template("confirmation_mails/confirmation.txt", name=current_user.username,
                                          token=token)
        html_body = render_template("confirmation_mails/confirmation.html", name=current_user.username, token=token)
        send_mail("Please confirm your email", sender=current_app.config.get('MAIL_USERNAME'),
                  recipient=current_user.email,
                  plain_text_body=plain_text_body, html_body=html_body)
        flash(_("We successfully registered you. But you need to verify your email through the link we sent you"), "success")
        return redirect(url_for('main_bp.secret'))
    return render_template("register.html", form=form,page_header_title=_("Register"))


@auth_bp.route('/<lang>/confirm/<token>')
@login_required
def confirm(token):
    if confirm_token(token, current_user.email, expiration=3600):
        current_user.is_confirmed = True
        current_user.confirmed_on = datetime.datetime.now()
        db.session.add(current_user)
        db.session.commit()
    return redirect(url_for('main_bp.secret'))


@auth_bp.route("/<lang>/resend_confirmation")
def resend_confirmation():
    token = generate_token(current_user.email)
    plain_text_body = render_template("confirmation_mails/confirmation.txt", name=current_user.username,
                                      token=token)
    html_body = render_template("confirmation_mails/confirmation.html", name=current_user.username, token=token)
    send_mail("Please confirm your email", sender=current_app.config.get('MAIL_USERNAME'),
              recipient=current_user.email,
              plain_text_body=plain_text_body, html_body=html_body)
    flash(_("Resent confirmation url to your email"), "success")
    return redirect(url_for('main_bp.secret'))


@auth_bp.route('/<lang>/unconfirmed')
def unconfirmed():
    return render_template("unconfirmed.html",page_header_title=_("Unconfirmed"))


@auth_bp.route('/<lang>/profile')
@login_required
def profile():
    return render_template("profile.html",page_header_title=_("Account"))


@auth_bp.route('/<lang>/send_reset_link', methods=['GET', 'POST'])
def send_reset_link():
    form = ResetPasswordSendLinkForm()
    if form.validate_on_submit():
        token = generate_token(form.email.data)
        plain_text_body = render_template("reset_password/reset_password.txt", token=token)
        html_body = render_template("reset_password/reset_password.html", token=token)
        send_mail("Reset password for Flasky", sender=current_app.config.get('MAIL_USERNAME'),
                  recipient=form.email.data,
                  plain_text_body=plain_text_body, html_body=html_body)
        flash(_("Sent reset password link to %(email)s",email=form.email.data), "success")
        return redirect(url_for('main_bp.home'))
    return render_template("send_reset_password_link.html", form=form,page_header_title=_("Send password reset link"))


@auth_bp.route("/<lang>/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    user = confirm_reset_password_token(token,expiration=3600)
    if user:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            user.password = form.new_password.data
            db.session.add(user)
            db.session.commit()
            flash(_("Updated your password successfully"), "success")
            login_user(user)
            return redirect(url_for('main_bp.secret'))
        return render_template("reset_password.html", form=form)
    else:
        flash(_("The reset link has expired or you are not authorized"), "danger")
        return redirect(url_for('auth_bp.login'))
