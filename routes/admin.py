from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy import or_

from models import (
    ActivityLog,
    ContactMessage,
    Experience,
    Project,
    Skill,
    db,
)

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
)


@admin_bp.app_context_processor
def inject_admin_message_count():
    if not current_user.is_authenticated:
        return {"unread_message_count": 0}

    unread_count = ContactMessage.query.filter_by(
        user_id=current_user.id,
        is_read=False,
    ).count()

    return {"unread_message_count": unread_count}


@admin_bp.route("/")
@login_required
def index():
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    statistics = {
        "total_skills": Skill.query.filter_by(user_id=current_user.id).count(),
        "total_experiences": Experience.query.filter_by(
            user_id=current_user.id
        ).count(),
        "total_projects": Project.query.filter_by(user_id=current_user.id).count(),
        "total_messages": ContactMessage.query.filter_by(
            user_id=current_user.id
        ).count(),
        "unread_messages": ContactMessage.query.filter_by(
            user_id=current_user.id,
            is_read=False,
        ).count(),
    }

    recent_activities = (
        ActivityLog.query.filter_by(user_id=current_user.id)
        .order_by(ActivityLog.created_at.desc())
        .limit(6)
        .all()
    )

    return render_template(
        "admin/dashboard.html",
        statistics=statistics,
        recent_activities=recent_activities,
    )


@admin_bp.get("/messages")
@login_required
def messages():
    search = request.args.get("q", "").strip()
    status = request.args.get("status", "all").strip().lower()

    message_query = ContactMessage.query.filter_by(user_id=current_user.id)

    if status == "unread":
        message_query = message_query.filter_by(is_read=False)
    elif status == "read":
        message_query = message_query.filter_by(is_read=True)

    if search:
        search_pattern = f"%{search}%"
        message_query = message_query.filter(
            or_(
                ContactMessage.name.ilike(search_pattern),
                ContactMessage.sender_email.ilike(search_pattern),
                ContactMessage.subject.ilike(search_pattern),
                ContactMessage.message.ilike(search_pattern),
            )
        )

    contact_messages = message_query.order_by(ContactMessage.created_at.desc()).all()

    total_messages = ContactMessage.query.filter_by(user_id=current_user.id).count()
    unread_messages = ContactMessage.query.filter_by(
        user_id=current_user.id,
        is_read=False,
    ).count()

    return render_template(
        "admin/messages.html",
        contact_messages=contact_messages,
        total_messages=total_messages,
        unread_messages=unread_messages,
        search=search,
        status=status,
    )


@admin_bp.post("/messages/<int:message_id>/toggle-read")
@login_required
def toggle_message_read(message_id):
    contact_message = ContactMessage.query.filter_by(
        id=message_id,
        user_id=current_user.id,
    ).first_or_404()

    contact_message.is_read = not contact_message.is_read

    try:
        db.session.commit()
        flash(
            "Status pesan berhasil diperbarui.",
            "success",
        )
    except Exception:
        db.session.rollback()
        flash(
            "Status pesan gagal diperbarui.",
            "danger",
        )

    return redirect(request.referrer or url_for("admin.messages"))


@admin_bp.post("/messages/<int:message_id>/delete")
@login_required
def delete_message(message_id):
    contact_message = ContactMessage.query.filter_by(
        id=message_id,
        user_id=current_user.id,
    ).first_or_404()

    try:
        db.session.delete(contact_message)
        db.session.commit()
        flash("Pesan berhasil dihapus.", "success")
    except Exception:
        db.session.rollback()
        flash("Pesan gagal dihapus.", "danger")

    return redirect(url_for("admin.messages"))
