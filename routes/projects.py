from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import Project, db
from utils.activity_logger import record_activity
from utils.cloudinary_uploader import (
    delete_cloudinary_image,
    upload_project_image,
)


projects_bp = Blueprint(
    "projects",
    __name__,
    url_prefix="/admin/projects",
)


def clean_value(value):
    if value is None:
        return ""

    return value.strip()


@projects_bp.route("/", methods=["GET", "POST"])
@login_required
def manage_projects():
    if request.method == "POST":
        judul = clean_value(request.form.get("judul"))
        deskripsi = clean_value(request.form.get("deskripsi"))
        link_project = clean_value(
            request.form.get("link_project")
        )
        gambar_file = request.files.get("gambar_file")

        if not judul:
            flash(
                "Judul proyek wajib diisi.",
                "warning",
            )
            return redirect(
                url_for("projects.manage_projects")
            )

        if len(judul) > 100:
            flash(
                "Judul proyek maksimal 100 karakter.",
                "warning",
            )
            return redirect(
                url_for("projects.manage_projects")
            )

        if len(deskripsi) > 400:
            flash(
                "Deskripsi maksimal 400 karakter.",
                "warning",
            )
            return redirect(
                url_for("projects.manage_projects")
            )

        if len(link_project) > 255:
            flash(
                "Link proyek maksimal 255 karakter.",
                "warning",
            )
            return redirect(
                url_for("projects.manage_projects")
            )

        gambar_url = None
        gambar_public_id = None

        # Upload gambar hanya jika admin memilih file.
        if gambar_file and gambar_file.filename:
            try:
                (
                    gambar_url,
                    gambar_public_id,
                ) = upload_project_image(
                    gambar_file
                )

            except ValueError as error:
                flash(
                    str(error),
                    "warning",
                )
                return redirect(
                    url_for("projects.manage_projects")
                )

            except Exception as error:
                print(
                    "Cloudinary upload error:",
                    error,
                )

                flash(
                    "Gambar gagal diunggah ke Cloudinary.",
                    "danger",
                )
                return redirect(
                    url_for("projects.manage_projects")
                )

        project = Project(
            user_id=current_user.id,
            judul=judul,
            deskripsi=deskripsi or None,
            gambar_url=gambar_url,
            gambar_public_id=gambar_public_id,
            link_project=link_project or None,
        )

        try:
            db.session.add(project)

            record_activity(
                user_id=current_user.id,
                action="create",
                entity_type="Proyek",
                entity_name=judul,
                description=(
                    f"Menambahkan proyek {judul}."
                ),
            )

            db.session.commit()

            flash(
                "Proyek berhasil ditambahkan.",
                "success",
            )

        except Exception as error:
            db.session.rollback()

            # Hapus gambar yang telanjur diunggah
            # apabila penyimpanan database gagal.
            if gambar_public_id:
                try:
                    delete_cloudinary_image(
                        gambar_public_id
                    )
                except Exception as cleanup_error:
                    print(
                        "Cloudinary cleanup error:",
                        cleanup_error,
                    )

            print(
                "Create project error:",
                error,
            )

            flash(
                "Proyek gagal ditambahkan.",
                "danger",
            )

        return redirect(
            url_for("projects.manage_projects")
        )

    project_list = (
        Project.query
        .filter_by(user_id=current_user.id)
        .order_by(Project.id.desc())
        .all()
    )

    return render_template(
        "admin/projects.html",
        projects=project_list,
    )


@projects_bp.route(
    "/<int:project_id>/edit",
    methods=["GET", "POST"],
)
@login_required
def edit_project(project_id):
    project = Project.query.filter_by(
        id=project_id,
        user_id=current_user.id,
    ).first_or_404()

    if request.method == "POST":
        judul = clean_value(
            request.form.get("judul")
        )
        deskripsi = clean_value(
            request.form.get("deskripsi")
        )
        link_project = clean_value(
            request.form.get("link_project")
        )
        gambar_file = request.files.get(
            "gambar_file"
        )

        if not judul:
            flash(
                "Judul proyek wajib diisi.",
                "warning",
            )
            return render_template(
                "admin/edit_project.html",
                project=project,
            )

        if len(judul) > 100:
            flash(
                "Judul proyek maksimal 100 karakter.",
                "warning",
            )
            return render_template(
                "admin/edit_project.html",
                project=project,
            )

        if len(deskripsi) > 400:
            flash(
                "Deskripsi maksimal 400 karakter.",
                "warning",
            )
            return render_template(
                "admin/edit_project.html",
                project=project,
            )

        if len(link_project) > 255:
            flash(
                "Link proyek maksimal 255 karakter.",
                "warning",
            )
            return render_template(
                "admin/edit_project.html",
                project=project,
            )

        old_public_id = project.gambar_public_id
        new_public_id = None
        new_gambar_url = None

        # Gambar lama tetap digunakan jika admin
        # tidak memilih gambar pengganti.
        if gambar_file and gambar_file.filename:
            try:
                (
                    new_gambar_url,
                    new_public_id,
                ) = upload_project_image(
                    gambar_file
                )

            except ValueError as error:
                flash(
                    str(error),
                    "warning",
                )
                return render_template(
                    "admin/edit_project.html",
                    project=project,
                )

            except Exception as error:
                print(
                    "Cloudinary update upload error:",
                    error,
                )

                flash(
                    "Gambar baru gagal diunggah.",
                    "danger",
                )
                return render_template(
                    "admin/edit_project.html",
                    project=project,
                )

        project.judul = judul
        project.deskripsi = deskripsi or None
        project.link_project = link_project or None

        if new_gambar_url and new_public_id:
            project.gambar_url = new_gambar_url
            project.gambar_public_id = new_public_id

        try:
            record_activity(
                user_id=current_user.id,
                action="update",
                entity_type="Proyek",
                entity_name=judul,
                description=(
                    f"Memperbarui proyek {judul}."
                ),
            )

            db.session.commit()

            # Setelah database berhasil diperbarui,
            # hapus gambar lama dari Cloudinary.
            if (
                new_public_id
                and old_public_id
                and old_public_id != new_public_id
            ):
                try:
                    delete_cloudinary_image(
                        old_public_id
                    )
                except Exception as delete_error:
                    print(
                        "Delete old Cloudinary image error:",
                        delete_error,
                    )

            flash(
                "Proyek berhasil diperbarui.",
                "success",
            )

            return redirect(
                url_for("projects.manage_projects")
            )

        except Exception as error:
            db.session.rollback()

            # Gambar baru dibersihkan jika database gagal.
            if new_public_id:
                try:
                    delete_cloudinary_image(
                        new_public_id
                    )
                except Exception as cleanup_error:
                    print(
                        "Cloudinary cleanup error:",
                        cleanup_error,
                    )

            print(
                "Update project error:",
                error,
            )

            flash(
                "Proyek gagal diperbarui.",
                "danger",
            )

    return render_template(
        "admin/edit_project.html",
        project=project,
    )


@projects_bp.post("/<int:project_id>/delete")
@login_required
def delete_project(project_id):
    project = Project.query.filter_by(
        id=project_id,
        user_id=current_user.id,
    ).first_or_404()

    project_title = project.judul
    project_public_id = project.gambar_public_id

    try:
        db.session.delete(project)

        record_activity(
            user_id=current_user.id,
            action="delete",
            entity_type="Proyek",
            entity_name=project_title,
            description=(
                f"Menghapus proyek {project_title}."
            ),
        )

        db.session.commit()

        # Hapus gambar setelah data database
        # berhasil dihapus.
        if project_public_id:
            try:
                delete_cloudinary_image(
                    project_public_id
                )
            except Exception as delete_error:
                print(
                    "Cloudinary delete error:",
                    delete_error,
                )

        flash(
            f"Proyek '{project_title}' berhasil dihapus.",
            "success",
        )

    except Exception as error:
        db.session.rollback()

        print(
            "Delete project error:",
            error,
        )

        flash(
            "Proyek gagal dihapus.",
            "danger",
        )

    return redirect(
        url_for("projects.manage_projects")
    )