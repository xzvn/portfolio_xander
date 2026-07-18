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


DEFAULT_ABOUT_HEADLINE = (
    "Mengenal saya dan perjalanan "
    "yang sedang saya bangun."
)


@profile_bp.route(
    "/about-headline/",
    methods=["GET", "POST"],
)
@login_required
def manage_about_headline():
    profile = Profile.query.filter_by(
        user_id=current_user.id
    ).first()

    if profile is None:
        flash(
            "Lengkapi profil terlebih dahulu "
            "sebelum mengatur headline About.",
            "warning",
        )

        return redirect(
            url_for("profile.manage_profile")
        )

    if request.method == "POST":
        about_headline = (
            request.form.get(
                "about_headline",
                "",
            )
            .strip()
        )

        if not about_headline:
            flash(
                "Headline About wajib diisi.",
                "warning",
            )

            return render_template(
                "admin/about_headline.html",
                profile=profile,
                default_headline=(
                    DEFAULT_ABOUT_HEADLINE
                ),
            )

        if len(about_headline) > 180:
            flash(
                "Headline About maksimal "
                "180 karakter.",
                "warning",
            )

            return render_template(
                "admin/about_headline.html",
                profile=profile,
                default_headline=(
                    DEFAULT_ABOUT_HEADLINE
                ),
            )

        profile.about_headline = about_headline

        try:
            record_activity(
                user_id=current_user.id,
                action="update",
                entity_type="Konten About",
                entity_name="Headline About",
                description=(
                    "Memperbarui headline "
                    "halaman About."
                ),
            )

            db.session.commit()

            flash(
                "Headline About berhasil diperbarui.",
                "success",
            )

        except Exception as error:
            db.session.rollback()

            print(
                "About headline error:",
                error,
            )

            flash(
                "Headline About gagal disimpan. "
                "Silakan coba kembali.",
                "danger",
            )

        return redirect(
            url_for(
                "profile.manage_about_headline"
            )
        )

    return render_template(
        "admin/about_headline.html",
        profile=profile,
        default_headline=DEFAULT_ABOUT_HEADLINE,
    )

PAGE_HEADLINE_DEFAULTS = {
    "about_headline": "Mengenal saya dan perjalanan yang sedang saya bangun.",
    "skills_headline": "Kemampuan yang terus saya pelajari dan kembangkan.",
    "experience_headline": "Pengalaman yang membentuk proses belajar saya.",
    "projects_headline": "Proyek yang dibangun dari proses belajar dan eksplorasi.",
    "contact_headline": "Mari berdiskusi dan membangun sesuatu yang bermanfaat.",
}


def build_page_headline_definitions(profile):
    home_default = profile.nama_lengkap if profile and profile.nama_lengkap else "Portfolio Xander"
    data = [
        {"key":"home","field":"home_headline","name":"Home","path":"/","endpoint":"home","icon":"house","title":"Headline halaman Home","description":"Judul utama pada hero halaman awal.","default":home_default,"presets":[home_default,"Membangun solusi digital melalui proses belajar yang nyata.","Belajar teknologi, mengembangkan ide, dan menciptakan karya."]},
        {"key":"about","field":"about_headline","name":"About","path":"/about","endpoint":"about","icon":"user-round","title":"Headline halaman Tentang","description":"Judul yang memperkenalkan diri dan perjalanan personal.","default":PAGE_HEADLINE_DEFAULTS["about_headline"],"presets":[PAGE_HEADLINE_DEFAULTS["about_headline"],"Belajar, bertumbuh, dan membangun arah melalui teknologi.","Cerita di balik proses belajar dan karya yang saya bangun."]},
        {"key":"skills","field":"skills_headline","name":"Skills","path":"/skills","endpoint":"skills","icon":"badge-check","title":"Headline halaman Skills","description":"Judul yang menjelaskan kemampuan dan pengembangan keahlian.","default":PAGE_HEADLINE_DEFAULTS["skills_headline"],"presets":[PAGE_HEADLINE_DEFAULTS["skills_headline"],"Keahlian yang saya gunakan untuk mengubah ide menjadi solusi.","Kemampuan teknis yang tumbuh melalui latihan dan proyek."]},
        {"key":"experience","field":"experience_headline","name":"Pengalaman","path":"/experience","endpoint":"experience","icon":"briefcase-business","title":"Headline halaman Pengalaman","description":"Judul perjalanan akademik, organisasi, dan profesional.","default":PAGE_HEADLINE_DEFAULTS["experience_headline"],"presets":[PAGE_HEADLINE_DEFAULTS["experience_headline"],"Perjalanan yang mengajarkan tanggung jawab dan kolaborasi.","Pengalaman yang memperkuat cara saya belajar dan bekerja."]},
        {"key":"projects","field":"projects_headline","name":"Proyek","path":"/projects","endpoint":"projects","icon":"folder-kanban","title":"Headline halaman Proyek","description":"Judul utama untuk memperkenalkan hasil karya.","default":PAGE_HEADLINE_DEFAULTS["projects_headline"],"presets":[PAGE_HEADLINE_DEFAULTS["projects_headline"],"Karya digital yang lahir dari masalah, ide, dan eksperimen.","Proyek yang menunjukkan proses berpikir dan kemampuan saya."]},
        {"key":"contact","field":"contact_headline","name":"Contact","path":"/contact","endpoint":"contact","icon":"messages-square","title":"Headline halaman Kontak","description":"Ajakan utama untuk memulai diskusi atau kolaborasi.","default":PAGE_HEADLINE_DEFAULTS["contact_headline"],"presets":[PAGE_HEADLINE_DEFAULTS["contact_headline"],"Mari bertukar gagasan dan menciptakan sesuatu bersama.","Terbuka untuk diskusi, kolaborasi, dan kesempatan baru."]},
    ]
    for page in data:
        current=getattr(profile,page["field"],None)
        page["value"]=current.strip() if current else page["default"]
        page["url"]=url_for(page["endpoint"])
    return data


@profile_bp.route("/page-headlines/", methods=["GET", "POST"])
@login_required
def manage_page_headlines():
    profile=Profile.query.filter_by(user_id=current_user.id).first()
    if profile is None:
        flash("Lengkapi profil terlebih dahulu sebelum mengatur headline pages.","warning")
        return redirect(url_for("profile.manage_profile"))
    pages=build_page_headline_definitions(profile)
    config={page["key"]:{"name":page["name"],"url":page["url"],"description":page["description"],"default":page["default"]} for page in pages}
    if request.method == "POST":
        values={}
        for page in pages:
            value=request.form.get(page["field"],"").strip()
            if not value:
                flash(f"Headline {page['name']} wajib diisi.","warning")
                return render_template("admin/page_headlines.html",profile=profile,page_definitions=pages,page_configuration=config)
            if len(value)>180:
                flash(f"Headline {page['name']} maksimal 180 karakter.","warning")
                return render_template("admin/page_headlines.html",profile=profile,page_definitions=pages,page_configuration=config)
            values[page["field"]]=value
        for field,value in values.items(): setattr(profile,field,value)
        try:
            record_activity(user_id=current_user.id,action="update",entity_type="Konten Portfolio",entity_name="Headline Pages",description="Memperbarui headline seluruh halaman portfolio.")
            db.session.commit(); flash("Seluruh headline pages berhasil diperbarui.","success")
        except Exception as error:
            db.session.rollback(); print("Page headlines error:",error); flash("Headline pages gagal disimpan. Silakan coba kembali.","danger")
        return redirect(url_for("profile.manage_page_headlines"))
    return render_template("admin/page_headlines.html",profile=profile,page_definitions=pages,page_configuration=config)

