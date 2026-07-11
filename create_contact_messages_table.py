from app import app
from models import ContactMessage, db


with app.app_context():
    ContactMessage.__table__.create(
        bind=db.engine,
        checkfirst=True,
    )

    print("Tabel contact_messages siap digunakan.")
