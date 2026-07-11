from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import Experience, db
from utils.activity_logger import record_activity


experiences_bp = Blueprint(
    "experiences",
    __name__,
    url_prefix="/admin/experiences",
)


def clean_value(value):
    if value is None:
        return ""

    return value.strip()


@experiences_bp.route("/", methods=["GET", "POST"])
@login_required
def manage_experiences():
    if request.method == "POST":
        print("POST TAMBAH PENGALAMAN DITERIMA")
        posisi = clean_value(request.form.get("posisi"))
        perusahaan = clean_value(request.form.get("perusahaan"))
        durasi = clean_value(request.form.get("durasi"))
        deskripsi = clean_value(request.form.get("deskripsi"))

        if not posisi:
            flash(
                "Posisi atau jabatan wajib diisi.",
                "warning",
            )
            return redirect(
                url_for("experiences.manage_experiences")
            )

        if not perusahaan:
            flash(
                "Nama perusahaan atau organisasi wajib diisi.",
                "warning",
            )
            return redirect(
                url_for("experiences.manage_experiences")
            )

        if len(posisi) > 100:
            flash(
                "Posisi maksimal 100 karakter.",
                "warning",
            )
            return redirect(
                url_for("experiences.manage_experiences")
            )

        if len(perusahaan) > 100:
            flash(
                "Nama perusahaan atau organisasi maksimal 100 karakter.",
                "warning",
            )
            return redirect(
                url_for("experiences.manage_experiences")
            )

        if len(durasi) > 50:
            flash(
                "Durasi maksimal 50 karakter.",
                "warning",
            )
            return redirect(
                url_for("experiences.manage_experiences")
            )

        if len(deskripsi) > 400:
            flash(
                "Deskripsi maksimal 400 karakter.",
                "warning",
            )
            return redirect(
                url_for("experiences.manage_experiences")
            )

        experience = Experience(
            user_id=current_user.id,
            posisi=posisi,
            perusahaan=perusahaan,
            durasi=durasi or None,
            deskripsi=deskripsi or None,
        )

        try:
            db.session.add(experience)

            record_activity(
                user_id=current_user.id,
                action="create",
                entity_type="Pengalaman",
                entity_name=posisi,
                description=(
                    f"Menambahkan pengalaman {posisi} "
                    f"di {perusahaan}."
                ),
            )

            db.session.commit()

            flash(
                "Pengalaman berhasil ditambahkan.",
                "success",
            )

        except Exception as error:
            db.session.rollback()

            print(f"Create experience error: {error}")

            flash(
                "Pengalaman gagal ditambahkan.",
                "danger",
            )

        return redirect(
            url_for("experiences.manage_experiences")
        )

    experience_list = (
        Experience.query
        .filter_by(user_id=current_user.id)
        .order_by(Experience.id.desc())
        .all()
    )

    return render_template(
        "admin/experiences.html",
        experiences=experience_list,
    )


@experiences_bp.route(
    "/<int:experience_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_experience(experience_id):
    experience = Experience.query.filter_by(
        id=experience_id,
        user_id=current_user.id,
    ).first_or_404()

    if request.method == "POST":
        posisi = clean_value(request.form.get("posisi"))
        perusahaan = clean_value(request.form.get("perusahaan"))
        durasi = clean_value(request.form.get("durasi"))
        deskripsi = clean_value(request.form.get("deskripsi"))

        if not posisi or not perusahaan:
            flash(
                "Posisi dan perusahaan atau organisasi wajib diisi.",
                "warning",
            )

            return render_template(
                "admin/edit_experience.html",
                experience=experience,
            )

        if len(posisi) > 100 or len(perusahaan) > 100:
            flash(
                "Posisi dan perusahaan maksimal 100 karakter.",
                "warning",
            )

            return render_template(
                "admin/edit_experience.html",
                experience=experience,
            )

        if len(durasi) > 50:
            flash(
                "Durasi maksimal 50 karakter.",
                "warning",
            )

            return render_template(
                "admin/edit_experience.html",
                experience=experience,
            )

        if len(deskripsi) > 400:
            flash(
                "Deskripsi maksimal 400 karakter.",
                "warning",
            )

            return render_template(
                "admin/edit_experience.html",
                experience=experience,
            )

        experience.posisi = posisi
        experience.perusahaan = perusahaan
        experience.durasi = durasi or None
        experience.deskripsi = deskripsi or None

        try:
            record_activity(
                user_id=current_user.id,
                action="update",
                entity_type="Pengalaman",
                entity_name=posisi,
                description=(
                    f"Memperbarui pengalaman {posisi} "
                    f"di {perusahaan}."
                ),
            )

            db.session.commit()

            flash(
                "Pengalaman berhasil diperbarui.",
                "success",
            )

            return redirect(
                url_for("experiences.manage_experiences")
            )

        except Exception as error:
            db.session.rollback()

            print(f"Update experience error: {error}")

            flash(
                "Pengalaman gagal diperbarui.",
                "danger",
            )

    return render_template(
        "admin/edit_experience.html",
        experience=experience,
    )


@experiences_bp.post("/<int:experience_id>/delete")
@login_required
def delete_experience(experience_id):
    experience = Experience.query.filter_by(
        id=experience_id,
        user_id=current_user.id,
    ).first_or_404()

    experience_position = experience.posisi
    experience_company = experience.perusahaan

    try:
        db.session.delete(experience)

        record_activity(
            user_id=current_user.id,
            action="delete",
            entity_type="Pengalaman",
            entity_name=experience_position,
            description=(
                f"Menghapus pengalaman {experience_position} "
                f"di {experience_company}."
            ),
        )

        db.session.commit()

        flash(
            f"Pengalaman '{experience_position}' berhasil dihapus.",
            "success",
        )

    except Exception as error:
        db.session.rollback()

        print(f"Delete experience error: {error}")

        flash(
            "Pengalaman gagal dihapus.",
            "danger",
        )

    return redirect(
        url_for("experiences.manage_experiences")
    )