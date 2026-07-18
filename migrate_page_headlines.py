from sqlalchemy import inspect, text
from app import app
from models import Profile, db

COLUMNS = {
    "home_headline": "VARCHAR(180) NULL",
    "about_headline": "VARCHAR(180) NULL",
    "skills_headline": "VARCHAR(180) NULL",
    "experience_headline": "VARCHAR(180) NULL",
    "projects_headline": "VARCHAR(180) NULL",
    "contact_headline": "VARCHAR(180) NULL",
}
DEFAULTS = {
    "about_headline": "Mengenal saya dan perjalanan yang sedang saya bangun.",
    "skills_headline": "Kemampuan yang terus saya pelajari dan kembangkan.",
    "experience_headline": "Pengalaman yang membentuk proses belajar saya.",
    "projects_headline": "Proyek yang dibangun dari proses belajar dan eksplorasi.",
    "contact_headline": "Mari berdiskusi dan membangun sesuatu yang bermanfaat.",
}

def migrate_page_headlines():
    with app.app_context():
        existing={column["name"] for column in inspect(db.engine).get_columns(Profile.__tablename__)}
        for name,definition in COLUMNS.items():
            if name in existing:
                print(f"Kolom profiles.{name} sudah tersedia.")
                continue
            db.session.execute(text(f"ALTER TABLE profiles ADD COLUMN {name} {definition}"))
            db.session.commit()
            print(f"Kolom profiles.{name} berhasil ditambahkan.")
        db.session.execute(text("UPDATE profiles SET home_headline = nama_lengkap WHERE home_headline IS NULL OR TRIM(home_headline) = ''"))
        for name,value in DEFAULTS.items():
            db.session.execute(text(f"UPDATE profiles SET {name} = :value WHERE {name} IS NULL OR TRIM({name}) = ''"),{"value":value})
        db.session.commit()
        print("Nilai awal seluruh headline berhasil disiapkan.")

if __name__ == "__main__":
    migrate_page_headlines()
