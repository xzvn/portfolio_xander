from sqlalchemy import inspect, text

from app import app
from models import Profile, db


DEFAULT_HEADLINE = (
    "Mengenal saya dan perjalanan "
    "yang sedang saya bangun."
)


def migrate_about_headline():
    with app.app_context():
        inspector = inspect(db.engine)

        column_names = {
            column["name"]
            for column in inspector.get_columns(
                Profile.__tablename__
            )
        }

        if "about_headline" not in column_names:
            db.session.execute(
                text(
                    """
                    ALTER TABLE profiles
                    ADD COLUMN about_headline
                    VARCHAR(180) NULL
                    """
                )
            )

            db.session.commit()

            print(
                "Kolom profiles.about_headline "
                "berhasil ditambahkan."
            )
        else:
            print(
                "Kolom profiles.about_headline "
                "sudah tersedia."
            )

        db.session.execute(
            text(
                """
                UPDATE profiles
                SET about_headline = :default_headline
                WHERE about_headline IS NULL
                   OR TRIM(about_headline) = ''
                """
            ),
            {
                "default_headline": DEFAULT_HEADLINE,
            },
        )

        db.session.commit()

        print(
            "Nilai awal headline About "
            "berhasil disiapkan."
        )


if __name__ == "__main__":
    migrate_about_headline()
