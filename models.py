from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import BIGINT

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
    )
    password_hash = db.Column(
        db.String(255),
        nullable=False,
    )
    role = db.Column(
        db.String(10),
        nullable=False,
        default="admin",
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    profile = db.relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    skills = db.relationship(
        "Skill",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    experiences = db.relationship(
        "Experience",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    projects = db.relationship(
        "Project",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    activity_logs = db.relationship(
        "ActivityLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    contact_messages = db.relationship(
        "ContactMessage",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Profile(db.Model):
    __tablename__ = "profiles"

    id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    user_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "users.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    nama_lengkap = db.Column(db.String(100), nullable=False)
    nama_panggilan = db.Column(db.String(50))
    tempat_lahir = db.Column(db.String(50))
    tanggal_lahir = db.Column(db.Date)
    email = db.Column(db.String(100))
    telepon = db.Column(db.String(20))
    universitas = db.Column(db.String(100))
    fakultas = db.Column(db.String(100))
    prodi = db.Column(db.String(100))
    semester = db.Column(db.String(20))
    alamat = db.Column(db.String(400))
    foto_url = db.Column(
        db.String(255),
    )

    foto_public_id = db.Column(
        db.String(255),
    )

    about_headline = db.Column(
        db.String(180),
    )

    home_headline = db.Column(
        db.String(180),
    )

    skills_headline = db.Column(
        db.String(180),
    )

    experience_headline = db.Column(
        db.String(180),
    )

    projects_headline = db.Column(
        db.String(180),
    )

    contact_headline = db.Column(
        db.String(180),
    )

    user = db.relationship(
        "User",
        back_populates="profile",
    )

    def __repr__(self):
        return f"<Profile {self.nama_lengkap}>"


class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    user_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "users.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    nama_skill = db.Column(
        db.String(50),
        nullable=False,
    )
    icon_class = db.Column(
        db.String(50),
    )

    persentase = db.Column(
        db.SmallInteger,
        nullable=False,
        default=75,
        server_default="75",
    )

    user = db.relationship(
        "User",
        back_populates="skills",
    )

    def __repr__(self):
        return f"<Skill {self.nama_skill}>"


class Experience(db.Model):
    __tablename__ = "experiences"

    id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    user_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "users.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    posisi = db.Column(
        db.String(100),
        nullable=False,
    )
    perusahaan = db.Column(
        db.String(100),
        nullable=False,
    )
    durasi = db.Column(db.String(50))
    deskripsi = db.Column(db.String(400))
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    user = db.relationship(
        "User",
        back_populates="experiences",
    )

    def __repr__(self):
        return f"<Experience {self.posisi}>"


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    user_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "users.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    judul = db.Column(
        db.String(100),
        nullable=False,
    )

    deskripsi = db.Column(
        db.String(400),
        nullable=True,
    )

    gambar_url = db.Column(
        db.String(255),
        nullable=True,
    )

    gambar_public_id = db.Column(
        db.String(255),
        nullable=True,
    )

    link_project = db.Column(
        db.String(255),
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    user = db.relationship(
        "User",
        back_populates="projects",
    )

    def __repr__(self):
        return f"<Project {self.judul}>"


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"

    id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    user_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "users.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    name = db.Column(db.String(100), nullable=False)
    sender_email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    email_id = db.Column(db.String(100))
    delivery_status = db.Column(
        db.String(20),
        nullable=False,
        default="pending",
        server_default="pending",
    )
    is_read = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default=db.text("0"),
        index=True,
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        index=True,
    )

    user = db.relationship(
        "User",
        back_populates="contact_messages",
    )

    def __repr__(self):
        return f"<ContactMessage {self.sender_email}>"


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(
        BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    user_id = db.Column(
        BIGINT(unsigned=True),
        db.ForeignKey(
            "users.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    action = db.Column(
        db.String(20),
        nullable=False,
    )

    entity_type = db.Column(
        db.String(50),
        nullable=False,
    )

    entity_name = db.Column(
        db.String(150),
    )

    description = db.Column(
        db.String(255),
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    user = db.relationship(
        "User",
        back_populates="activity_logs",
    )

    def __repr__(self):
        return f"<ActivityLog " f"{self.action} {self.entity_type}>"
