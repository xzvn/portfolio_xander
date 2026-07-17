from sqlalchemy import inspect, text
from app import app
from models import Skill, db


def add_skill_percentage_column():
    with app.app_context():
        columns = {column["name"] for column in inspect(db.engine).get_columns(Skill.__tablename__)}
        if "persentase" in columns:
            print("Kolom skills.persentase sudah tersedia. Tidak ada perubahan database.")
            return
        try:
            db.session.execute(text("""
                ALTER TABLE skills
                ADD COLUMN persentase TINYINT UNSIGNED NOT NULL DEFAULT 75
                AFTER icon_class
            """))
            db.session.commit()
            print("Kolom skills.persentase berhasil dibuat dengan nilai awal 75%.")
        except Exception as error:
            db.session.rollback()
            print("Gagal menambahkan kolom persentase.")
            print(f"Detail: {error}")
            raise


if __name__ == "__main__":
    add_skill_percentage_column()
