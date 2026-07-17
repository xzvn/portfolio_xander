from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import Skill, db

skills_bp = Blueprint(
    "skills",
    __name__,
    url_prefix="/admin/skills",
)


SKILL_ICONS = {
    "code-2": "Pemrograman",
    "braces": "Kode",
    "terminal": "Terminal",
    "file-code-2": "Web Development",
    "panels-top-left": "Frontend",
    "server": "Backend",
    "database": "Database",
    "chart-no-axes-column-increasing": "Data Analysis",
    "palette": "Desain",
    "figma": "UI/UX Design",
    "git-branch": "Version Control",
    "github": "GitHub",
    "cloud": "Cloud",
    "workflow": "Workflow",
    "settings-2": "Tools",
}


def clean_value(value):
    if value is None:
        return ""

    return value.strip()


def parse_percentage(value):
    try:
        percentage = int(str(value).strip())
    except (TypeError, ValueError):
        return None

    if percentage < 0 or percentage > 100:
        return None

    return percentage


@skills_bp.route("/", methods=["GET", "POST"])
@login_required
def manage_skills():
    if request.method == "POST":
        nama_skill = clean_value(request.form.get("nama_skill"))

        icon_class = clean_value(request.form.get("icon_class"))

        persentase = parse_percentage(
            request.form.get("persentase")
        )

        if not nama_skill:
            flash(
                "Nama skill wajib diisi.",
                "warning",
            )
            return redirect(url_for("skills.manage_skills"))

        if len(nama_skill) > 50:
            flash(
                "Nama skill maksimal 50 karakter.",
                "warning",
            )
            return redirect(url_for("skills.manage_skills"))

        if persentase is None:
            flash(
                "Persentase skill harus berupa angka 0 sampai 100.",
                "warning",
            )
            return redirect(url_for("skills.manage_skills"))

        if icon_class not in SKILL_ICONS:
            icon_class = "code-2"

        existing_skill = Skill.query.filter(
            Skill.user_id == current_user.id,
            db.func.lower(Skill.nama_skill) == nama_skill.lower(),
        ).first()

        if existing_skill:
            flash(
                f"Skill '{nama_skill}' sudah tersedia.",
                "warning",
            )
            return redirect(url_for("skills.manage_skills"))

        skill = Skill(
            user_id=current_user.id,
            nama_skill=nama_skill,
            icon_class=icon_class,
            persentase=persentase,
        )

        try:
            db.session.add(skill)
            db.session.commit()

            flash(
                "Skill berhasil ditambahkan.",
                "success",
            )

        except Exception as error:
            db.session.rollback()

            print(f"Create skill error: {error}")

            flash(
                "Skill gagal ditambahkan.",
                "danger",
            )

        return redirect(url_for("skills.manage_skills"))

    skill_list = (
        Skill.query.filter_by(user_id=current_user.id).order_by(Skill.id.desc()).all()
    )

    return render_template(
        "admin/skills.html",
        skills=skill_list,
        skill_icons=SKILL_ICONS,
    )


@skills_bp.route(
    "/<int:skill_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_skill(skill_id):
    skill = Skill.query.filter_by(
        id=skill_id,
        user_id=current_user.id,
    ).first_or_404()

    if request.method == "POST":
        nama_skill = clean_value(request.form.get("nama_skill"))

        icon_class = clean_value(request.form.get("icon_class"))

        persentase = parse_percentage(
            request.form.get("persentase")
        )

        if not nama_skill:
            flash(
                "Nama skill wajib diisi.",
                "warning",
            )

            return render_template(
                "admin/edit_skill.html",
                skill=skill,
                skill_icons=SKILL_ICONS,
            )

        if len(nama_skill) > 50:
            flash(
                "Nama skill maksimal 50 karakter.",
                "warning",
            )

            return render_template(
                "admin/edit_skill.html",
                skill=skill,
                skill_icons=SKILL_ICONS,
            )

        if persentase is None:
            flash(
                "Persentase skill harus berupa angka 0 sampai 100.",
                "warning",
            )

            return render_template(
                "admin/edit_skill.html",
                skill=skill,
                skill_icons=SKILL_ICONS,
            )

        duplicate_skill = Skill.query.filter(
            Skill.user_id == current_user.id,
            Skill.id != skill.id,
            db.func.lower(Skill.nama_skill) == nama_skill.lower(),
        ).first()

        if duplicate_skill:
            flash(
                f"Skill '{nama_skill}' sudah tersedia.",
                "warning",
            )

            return render_template(
                "admin/edit_skill.html",
                skill=skill,
                skill_icons=SKILL_ICONS,
            )

        if icon_class not in SKILL_ICONS:
            icon_class = "code-2"

        skill.nama_skill = nama_skill
        skill.icon_class = icon_class
        skill.persentase = persentase

        try:
            db.session.commit()

            flash(
                "Skill berhasil diperbarui.",
                "success",
            )

            return redirect(url_for("skills.manage_skills"))

        except Exception as error:
            db.session.rollback()

            print(f"Update skill error: {error}")

            flash(
                "Skill gagal diperbarui.",
                "danger",
            )

    return render_template(
        "admin/edit_skill.html",
        skill=skill,
        skill_icons=SKILL_ICONS,
    )


@skills_bp.post("/<int:skill_id>/delete")
@login_required
def delete_skill(skill_id):
    skill = Skill.query.filter_by(
        id=skill_id,
        user_id=current_user.id,
    ).first_or_404()

    try:
        db.session.delete(skill)
        db.session.commit()

        flash(
            f"Skill '{skill.nama_skill}' berhasil dihapus.",
            "success",
        )

    except Exception as error:
        db.session.rollback()

        print(f"Delete skill error: {error}")

        flash(
            "Skill gagal dihapus.",
            "danger",
        )

    return redirect(url_for("skills.manage_skills"))
