from flask import flash, redirect, url_for, render_template, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import desc, or_
from app.forms.book import DriftForm
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.user import User
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from . import web


@web.route(rule='/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)

    if current_gift.is_yourself_gift(current_user.id):
        flash(message='这本书是你自己的^_^，不能向自己索要书籍噢')
        return redirect(location=url_for('web.book_detail', isbn=current_gift.isbn))

    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        send_mail(to=current_gift.user.email, subject='有人想要一本书', template='email/get_gift.html', wisher=current_user, gift=current_gift)
        return redirect(location=url_for('web.pending'))

    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans, form=form)


@web.route(rule='/pending')
@login_required
def pending():
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id)).order_by(
        desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route(rule='/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid == current_user.id, Drift.id == did).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(location=url_for('web.pending'))


@web.route(rule='/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    # requester_id = current_user.id 防止超权
    with db.auto_commit():
        drift = Drift.query.filter_by(requester_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
    return redirect(location=url_for('web.pending'))


@web.route(rule='/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    """已邮寄"""
    with db.auto_commit():
        drift = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += current_app.config['BEANS_EVERY_DRIFT']
        gift = Gift.query.filter_by(id=drift.gift_id).first_or_404()
        gift.launched = True  # 将礼物状态改为True
        # Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id, launched=False).update({Wish.launched: True})
        wish = Wish.query.filter_by(isbn=drift.isbn, uid=drift.requester_id, launched=False).first_or_404()
        wish.launched = True  # 将心愿状态改为True
    return redirect(location=url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1

        db.session.add(drift)
