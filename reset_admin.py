from getpass import getpass

from werkzeug.security import generate_password_hash

from app import create_app
from models import User, db


app = create_app()


def reset_admin_password():
    with app.app_context():
        admins = (
            User.query.filter_by(role="admin")
            .order_by(User.id.asc())
            .all()
        )

        if not admins:
            print("Tidak ada akun admin di database.")
            return

        print("=" * 48)
        print("DAFTAR AKUN ADMIN")
        print("=" * 48)

        for number, admin in enumerate(admins, start=1):
            print(f"{number}. {admin.username} (ID: {admin.id})")

        print("=" * 48)

        while True:
            choice = input("Pilih nomor akun yang akan direset: ").strip()

            try:
                selected_index = int(choice) - 1
                selected_admin = admins[selected_index]
                break
            except (ValueError, IndexError):
                print("Pilihan tidak valid. Masukkan nomor pada daftar.")

        new_password = getpass("Masukkan password baru: ")
        confirmation = getpass("Konfirmasi password baru: ")

        if len(new_password) < 8:
            print("Password minimal 8 karakter.")
            return

        if new_password != confirmation:
            print("Konfirmasi password tidak sesuai.")
            return

        try:
            selected_admin.password_hash = generate_password_hash(new_password)
            db.session.commit()

            print("=" * 48)
            print("Password admin berhasil direset.")
            print(f"Username : {selected_admin.username}")
            print("Password : menggunakan password baru yang baru dimasukkan")
            print("=" * 48)

        except Exception as error:
            db.session.rollback()
            print("Password admin gagal direset.")
            print(f"Detail error: {error}")


if __name__ == "__main__":
    reset_admin_password()
