from getpass import getpass

from werkzeug.security import generate_password_hash

from app import create_app
from models import User, db


app = create_app()


def create_admin():
    with app.app_context():
        print("=" * 45)
        print("MEMBUAT AKUN ADMIN PORTFOLIO")
        print("=" * 45)

        username = input("Masukkan username admin: ").strip()

        if not username:
            print("Username tidak boleh kosong.")
            return

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            print(f"Username '{username}' sudah digunakan.")
            return

        password = getpass("Masukkan password admin: ")
        confirmation = getpass("Konfirmasi password admin: ")

        if len(password) < 8:
            print("Password minimal 8 karakter.")
            return

        if password != confirmation:
            print("Konfirmasi password tidak sesuai.")
            return

        admin = User(
            username=username,
            password_hash=generate_password_hash(password),
            role="admin",
        )

        try:
            db.session.add(admin)
            db.session.commit()

            print("=" * 45)
            print("Akun admin berhasil dibuat.")
            print(f"Username : {admin.username}")
            print(f"Role     : {admin.role}")
            print("=" * 45)

        except Exception as error:
            db.session.rollback()
            print("Akun admin gagal dibuat.")
            print(f"Detail error: {error}")


if __name__ == "__main__":
    create_admin()