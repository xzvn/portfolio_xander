from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from models import Profile, db
from utils.activity_logger import record_activity
from utils.cloudinary_uploader import (
    delete_cloudinary_image,
    upload_profile_image,
)


profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/admin/profile",
)


def empty_to_none(value):
    """Mengubah input kosong menjadi None."""
    if value is None:
        return None

    cleaned_value = value.strip()

    return cleaned_value if cleaned_value else None


@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def manage_profile():
    profile = Profile.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == "POST":
        profile_is_new = profile is None

        nama_lengkap = request.form.get(
            "nama_lengkap",
            "",
        ).strip()

        if not nama_lengkap:
            flash(
                "Nama lengkap wajib diisi.",
                "warning",
            )

            return render_template(
                "admin/profile.html",
                profile=profile,
            )

        if len(nama_lengkap) > 100:
            flash(
                "Nama lengkap maksimal 100 karakter.",
                "warning",
            )

            return render_template(
                "admin/profile.html",
                profile=profile,
            )

        tanggal_lahir_input = request.form.get(
            "tanggal_lahir",
            "",
        ).strip()

        tanggal_lahir = None

        if tanggal_lahir_input:
            try:
                tanggal_lahir = date.fromisoformat(
                    tanggal_lahir_input
                )

            except ValueError:
                flash(
                    "Format tanggal lahir tidak valid.",
                    "danger",
                )

                return render_template(
                    "admin/profile.html",
                    profile=profile,
                )

        foto_file = request.files.get("foto_file")

        old_foto_public_id = (
            profile.foto_public_id
            if profile
            else None
        )

        new_foto_url = None
        new_foto_public_id = None

        # Upload hanya jika admin memilih foto baru.
        if foto_file and foto_file.filename:
            try:
                (
                    new_foto_url,
                    new_foto_public_id,
                ) = upload_profile_image(
                    foto_file
                )

            except ValueError as error:
                flash(
                    str(error),
                    "warning",
                )

                return render_template(
                    "admin/profile.html",
                    profile=profile,
                )

            except Exception as error:
                print(
                    "Cloudinary profile upload error:",
                    error,
                )

                flash(
                    "Foto profil gagal diunggah ke Cloudinary.",
                    "danger",
                )

                return render_template(
                    "admin/profile.html",
                    profile=profile,
                )

        # Buat profil jika belum tersedia.
        if profile is None:
            profile = Profile(
                user_id=current_user.id,
                nama_lengkap=nama_lengkap,
            )

        profile.nama_lengkap = nama_lengkap

        profile.nama_panggilan = empty_to_none(
            request.form.get("nama_panggilan")
        )

        profile.tempat_lahir = empty_to_none(
            request.form.get("tempat_lahir")
        )

        profile.tanggal_lahir = tanggal_lahir

        profile.email = empty_to_none(
            request.form.get("email")
        )

        profile.telepon = empty_to_none(
            request.form.get("telepon")
        )

        profile.universitas = empty_to_none(
            request.form.get("universitas")
        )

        profile.fakultas = empty_to_none(
            request.form.get("fakultas")
        )

        profile.prodi = empty_to_none(
            request.form.get("prodi")
        )

        profile.semester = empty_to_none(
            request.form.get("semester")
        )

        profile.alamat = empty_to_none(
            request.form.get("alamat")
        )

        # Foto lama tetap digunakan jika tidak memilih foto baru.
        if new_foto_url and new_foto_public_id:
            profile.foto_url = new_foto_url
            profile.foto_public_id = new_foto_public_id

        try:
            db.session.add(profile)

            record_activity(
                user_id=current_user.id,
                action=(
                    "create"
                    if profile_is_new
                    else "update"
                ),
                entity_type="Profil",
                entity_name=nama_lengkap,
                description=(
                    f"Menambahkan data profil {nama_lengkap}."
                    if profile_is_new
                    else f"Memperbarui data profil {nama_lengkap}."
                ),
            )

            db.session.commit()

            # Foto lama dihapus setelah database berhasil disimpan.
            if (
                new_foto_public_id
                and old_foto_public_id
                and old_foto_public_id != new_foto_public_id
            ):
                try:
                    delete_cloudinary_image(
                        old_foto_public_id
                    )

                except Exception as delete_error:
                    print(
                        "Delete old profile image error:",
                        delete_error,
                    )

            flash(
                "Data profil berhasil disimpan.",
                "success",
            )

        except Exception as error:
            db.session.rollback()

            # Foto baru dibersihkan jika penyimpanan database gagal.
            if new_foto_public_id:
                try:
                    delete_cloudinary_image(
                        new_foto_public_id
                    )

                except Exception as cleanup_error:
                    print(
                        "Cloudinary profile cleanup error:",
                        cleanup_error,
                    )

            print(
                "Profile error:",
                error,
            )

            flash(
                "Data profil gagal disimpan. Silakan coba kembali.",
                "danger",
            )

        return redirect(
            url_for("profile.manage_profile")
        )

    return render_template(
        "admin/profile.html",
        profile=profile,
    )