-- =====================================================
-- DATABASE WEBSITE PORTOFOLIO
-- =====================================================

CREATE DATABASE IF NOT EXISTS portfolio_xander CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE portfolio_xander;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS projects;

DROP TABLE IF EXISTS experiences;

DROP TABLE IF EXISTS skills;

DROP TABLE IF EXISTS profiles;

DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- 1. TABEL USERS
-- Menyimpan akun admin
-- =====================================================

CREATE TABLE users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(10) NOT NULL DEFAULT 'admin',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY users_username_uk (username)
);

-- =====================================================
-- 2. TABEL PROFILES
-- Menyimpan data profil pemilik portofolio
-- =====================================================

CREATE TABLE profiles (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    nama_lengkap VARCHAR(100) NOT NULL,
    nama_panggilan VARCHAR(50),
    tempat_lahir VARCHAR(50),
    tanggal_lahir DATE,
    email VARCHAR(100),
    telepon VARCHAR(20),
    universitas VARCHAR(100),
    fakultas VARCHAR(100),
    prodi VARCHAR(100),
    semester VARCHAR(20),
    alamat VARCHAR(400),
    foto_url VARCHAR(255),
    PRIMARY KEY (id),
    UNIQUE KEY profiles_user_id_uk (user_id),
    CONSTRAINT profiles_users_fk FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- =====================================================
-- 3. TABEL SKILLS
-- Menyimpan kemampuan pengguna
-- =====================================================

CREATE TABLE skills (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    nama_skill VARCHAR(50) NOT NULL,
    icon_class VARCHAR(50),
    persentase TINYINT UNSIGNED NOT NULL DEFAULT 75,
    PRIMARY KEY (id),
    KEY skills_user_id_idx (user_id),
    CONSTRAINT skills_users_fk FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- =====================================================
-- 4. TABEL EXPERIENCES
-- Menyimpan pengalaman kerja atau organisasi
-- =====================================================

CREATE TABLE experiences (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    posisi VARCHAR(100) NOT NULL,
    perusahaan VARCHAR(100) NOT NULL,
    durasi VARCHAR(50),
    deskripsi VARCHAR(400),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY experiences_user_id_idx (user_id),
    CONSTRAINT experiences_users_fk FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- =====================================================
-- 5. TABEL PROJECTS
-- Menyimpan proyek portofolio
-- =====================================================

CREATE TABLE projects (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    judul VARCHAR(100) NOT NULL,
    deskripsi VARCHAR(400),
    gambar_url VARCHAR(255),
    link_project VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY projects_user_id_idx (user_id),
    CONSTRAINT projects_users_fk FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- =====================================================
-- CEK TABEL
-- =====================================================

SHOW TABLES;