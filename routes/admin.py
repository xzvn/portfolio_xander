from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_required

from models import ActivityLog, Experience, Project, Skill


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
)


@admin_bp.route("/")
@login_required
def index():
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    statistics = {
        "total_skills": Skill.query.filter_by(
            user_id=current_user.id
        ).count(),

        "total_experiences": Experience.query.filter_by(
            user_id=current_user.id
        ).count(),

        "total_projects": Project.query.filter_by(
            user_id=current_user.id
        ).count(),
    }

    recent_activities = (
        ActivityLog.query
        .filter_by(user_id=current_user.id)
        .order_by(ActivityLog.created_at.desc())
        .limit(6)
        .all()
    )

    print(
        "JUMLAH AKTIVITAS DASHBOARD:",
        len(recent_activities),
    )

    return render_template(
        "admin/dashboard.html",
        statistics=statistics,
        recent_activities=recent_activities,
    )