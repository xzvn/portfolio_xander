import re
from datetime import datetime
from pathlib import Path

import resend
from flask import (
    Flask,
    current_app,
    jsonify,
    render_template,
    request,
)
from flask_login import LoginManager
from jinja2 import TemplateNotFound
from markupsafe import escape
from sqlalchemy import text

from config import Config
from models import (
    Experience,
    Profile,
    Project,
    Skill,
    User,
    db,
)
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.experiences import experiences_bp
from routes.profile import profile_bp
from routes.projects import projects_bp
from routes.skills import skills_bp
from utils.cloudinary_config import configure_cloudinary

try:
    from template_loader import configure_template_loader
except (ImportError, ModuleNotFoundError):
    configure_template_loader = None


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

login_manager = LoginManager()


def create_app():
    app = Flask(
        __name__,
        template_folder=str(TEMPLATE_DIR),
        static_folder=str(STATIC_DIR),
        static_url_path="/static",
    )

    if configure_template_loader is not None:
        configure_template_loader(
            app,
            TEMPLATE_DIR,
        )

    app.config.from_object(Config)
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

    home_template = TEMPLATE_DIR / "public" / "home.html"
    print("BASE_DIR:", BASE_DIR)
    print("TEMPLATE_DIR:", TEMPLATE_DIR)
    print("HOME_TEMPLATE_EXISTS:", home_template.is_file())

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = (
        "Silakan login terlebih dahulu untuk membuka halaman admin."
    )
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (TypeError, ValueError):
            return None

    configure_cloudinary()

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(experiences_bp)
    app.register_blueprint(projects_bp)

    def get_public_data():
        owner = (
            User.query.filter_by(role="admin")
            .order_by(User.id.asc())
            .first()
        )

        profile = None
        public_skills = []
        public_experiences = []
        public_projects = []

        if owner:
            profile = Profile.query.filter_by(user_id=owner.id).first()

            public_skills = (
                Skill.query.filter_by(user_id=owner.id)
                .order_by(Skill.id.asc())
                .all()
            )

            public_experiences = (
                Experience.query.filter_by(user_id=owner.id)
                .order_by(Experience.id.desc())
                .all()
            )

            public_projects = (
                Project.query.filter_by(user_id=owner.id)
                .order_by(Project.id.desc())
                .all()
            )

        return {
            "profile": profile,
            "skills": public_skills,
            "experiences": public_experiences,
            "projects": public_projects,
            "current_year": datetime.now().year,
        }

    @app.get("/")
    def home():
        return render_template(
            "public/home.html",
            **get_public_data(),
        )

    @app.get("/about")
    def about():
        return render_template(
            "public/about.html",
            **get_public_data(),
        )

    @app.get("/skills")
    def skills():
        return render_template(
            "public/skills.html",
            **get_public_data(),
        )

    @app.get("/experience")
    def experience():
        return render_template(
            "public/experience.html",
            **get_public_data(),
        )

    @app.get("/projects")
    def projects():
        return render_template(
            "public/projects.html",
            **get_public_data(),
        )

    @app.get("/contact")
    def contact():
        return render_template(
            "public/contact.html",
            **get_public_data(),
        )

    @app.get("/health")
    def health():
        try:
            app.jinja_env.get_template("public/home.html")
            template_loaded = True
        except TemplateNotFound:
            template_loaded = False

        return jsonify(
            {
                "status": "ok",
                "template_loaded": template_loaded,
                "filesystem_template_exists": (
                    TEMPLATE_DIR / "public" / "home.html"
                ).is_file(),
                "embedded_loader_enabled": (
                    configure_template_loader is not None
                ),
            }
        )

    @app.post("/api/contact/send")
    def send_contact_email():
        data = request.get_json(silent=True) or {}

        name = str(data.get("name", "")).strip()
        sender_email = str(data.get("email", "")).strip()
        subject = str(data.get("subject", "")).strip()
        message = str(data.get("message", "")).strip()

        if not name:
            return jsonify(
                {
                    "status": "error",
                    "message": "Nama wajib diisi.",
                }
            ), 400

        email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

        if not re.fullmatch(email_pattern, sender_email):
            return jsonify(
                {
                    "status": "error",
                    "message": "Format email tidak valid.",
                }
            ), 400

        if not subject:
            return jsonify(
                {
                    "status": "error",
                    "message": "Subjek wajib diisi.",
                }
            ), 400

        if not message:
            return jsonify(
                {
                    "status": "error",
                    "message": "Pesan wajib diisi.",
                }
            ), 400

        if len(name) > 100:
            return jsonify(
                {
                    "status": "error",
                    "message": "Nama maksimal 100 karakter.",
                }
            ), 400

        if len(sender_email) > 150:
            return jsonify(
                {
                    "status": "error",
                    "message": "Email maksimal 150 karakter.",
                }
            ), 400

        if len(subject) > 150:
            return jsonify(
                {
                    "status": "error",
                    "message": "Subjek maksimal 150 karakter.",
                }
            ), 400

        if len(message) > 500:
            return jsonify(
                {
                    "status": "error",
                    "message": "Pesan maksimal 500 karakter.",
                }
            ), 400

        clean_subject = subject.replace("\r", " ").replace("\n", " ")

        safe_name = escape(name)
        safe_email = escape(sender_email)
        safe_subject = escape(clean_subject)
        safe_message = escape(message).replace("\n", "<br>")

        email_html = f"""
        <div style="margin:0;padding:24px;background:#f5f7fb;
                    font-family:Arial,sans-serif;color:#202a3c;">
            <div style="max-width:620px;margin:0 auto;overflow:hidden;
                        border:1px solid #e2e6ee;border-radius:18px;
                        background:#ffffff;">
                <div style="padding:24px;background:#182235;color:#ffffff;">
                    <p style="margin:0 0 8px;color:#aeb8ff;font-size:12px;
                              font-weight:bold;letter-spacing:1px;">
                        PESAN PORTFOLIO
                    </p>
                    <h1 style="margin:0;font-size:24px;">
                        Pesan baru dari halaman kontak
                    </h1>
                </div>
                <div style="padding:28px;">
                    <table style="width:100%;margin-bottom:24px;
                                  border-collapse:collapse;">
                        <tr>
                            <td style="width:110px;padding:8px 0;color:#687387;">
                                Nama
                            </td>
                            <td style="padding:8px 0;font-weight:bold;">
                                {safe_name}
                            </td>
                        </tr>
                        <tr>
                            <td style="padding:8px 0;color:#687387;">Email</td>
                            <td style="padding:8px 0;">{safe_email}</td>
                        </tr>
                        <tr>
                            <td style="padding:8px 0;color:#687387;">Subjek</td>
                            <td style="padding:8px 0;font-weight:bold;">
                                {safe_subject}
                            </td>
                        </tr>
                    </table>
                    <div style="padding:20px;border-left:4px solid #5869d7;
                                border-radius:10px;background:#eef0ff;
                                line-height:1.7;">
                        {safe_message}
                    </div>
                </div>
            </div>
        </div>
        """

        email_text = (
            "Pesan baru dari halaman kontak portfolio\n\n"
            f"Nama: {name}\n"
            f"Email: {sender_email}\n"
            f"Subjek: {clean_subject}\n\n"
            f"Pesan:\n{message}"
        )

        try:
            resend.api_key = current_app.config["RESEND_API_KEY"]

            params: resend.Emails.SendParams = {
                "from": current_app.config["RESEND_FROM_EMAIL"],
                "to": [current_app.config["CONTACT_RECEIVER_EMAIL"]],
                "subject": f"Portfolio Contact: {clean_subject}",
                "html": email_html,
                "text": email_text,
                "reply_to": sender_email,
            }

            result = resend.Emails.send(params)

            return jsonify(
                {
                    "status": "success",
                    "message": (
                        "Pesan berhasil dikirim. "
                        "Terima kasih telah menghubungi saya."
                    ),
                    "email_id": result.get("id"),
                }
            )

        except Exception:
            current_app.logger.exception(
                "Gagal mengirim email kontak melalui Resend."
            )

            return jsonify(
                {
                    "status": "error",
                    "message": (
                        "Pesan belum berhasil dikirim. "
                        "Silakan coba kembali."
                    ),
                }
            ), 500

    @app.get("/db-check")
    def database_check():
        try:
            result = db.session.execute(
                text(
                    """
                    SELECT
                        DATABASE() AS database_name,
                        VERSION() AS database_version
                    """
                )
            ).mappings().one()

            return jsonify(
                {
                    "status": "success",
                    "message": "Flask berhasil terhubung ke TiDB.",
                    "database": result["database_name"],
                    "version": result["database_version"],
                }
            )

        except Exception as error:
            db.session.rollback()

            return jsonify(
                {
                    "status": "error",
                    "message": "Flask gagal terhubung ke TiDB.",
                    "detail": str(error),
                }
            ), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
