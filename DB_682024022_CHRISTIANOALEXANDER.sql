-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: gateway01.ap-southeast-1.prod.alicloud.tidbcloud.com    Database: portfolio_xander
-- ------------------------------------------------------
-- Server version	8.0.11-TiDB-v8.5.3-serverless

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity_logs`
--

DROP TABLE IF EXISTS `activity_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_logs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `action` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `entity_type` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `entity_name` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  KEY `idx_activity_user_created` (`user_id`,`created_at`),
  CONSTRAINT `fk_activity_logs_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=355090;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_logs`
--

LOCK TABLES `activity_logs` WRITE;
/*!40000 ALTER TABLE `activity_logs` DISABLE KEYS */;
INSERT INTO `activity_logs` VALUES (1,1,'create','Pengalaman','Web developer','Menambahkan pengalaman Web developer di UKSW.','2026-07-10 07:48:56'),(30001,1,'create','Proyek','Pemrograman Web Modern','Menambahkan proyek Pemrograman Web Modern.','2026-07-10 08:27:42'),(30002,1,'delete','Proyek','Pemrograman Web Modern','Menghapus proyek Pemrograman Web Modern.','2026-07-10 08:27:53'),(60001,1,'create','Proyek','Buat Keraton','Menambahkan proyek Buat Keraton.','2026-07-10 08:58:24'),(90001,1,'update','Profil','Chris Eka','Memperbarui data profil Chris Eka.','2026-07-10 09:20:02'),(120001,1,'update','Profil','Christiano Alexander','Memperbarui data profil Christiano Alexander.','2026-07-10 12:36:06'),(150001,1,'update','Profil','Christiano Alexander','Memperbarui data profil Christiano Alexander.','2026-07-11 08:24:49'),(180001,1,'update','Profil','Christiano Alexander','Memperbarui data profil Christiano Alexander.','2026-07-11 09:53:36'),(210001,1,'update','Profil','Christiano Alexander','Memperbarui data profil Christiano Alexander.','2026-07-11 13:32:16'),(210002,1,'update','Profil','Christiano Alexander Eka Dian Putra Nugraha','Memperbarui data profil Christiano Alexander Eka Dian Putra Nugraha.','2026-07-11 13:33:46'),(210003,1,'update','Profil','Christiano Alexander','Memperbarui data profil Christiano Alexander.','2026-07-11 13:38:45'),(240001,1,'create','Proyek','Website Portofolio','Menambahkan proyek Website Portofolio.','2026-07-18 11:25:56'),(240002,1,'create','Proyek','Website Portofolio','Menambahkan proyek Website Portofolio.','2026-07-18 11:25:58'),(240003,1,'delete','Proyek','Website Portofolio','Menghapus proyek Website Portofolio.','2026-07-18 11:26:06'),(283885,1,'create','Proyek','Website Marketplace Jasa','Menambahkan proyek Website Marketplace Jasa.','2026-07-18 11:48:05'),(283886,1,'delete','Proyek','Buat Keraton','Menghapus proyek Buat Keraton.','2026-07-18 11:48:52'),(283887,1,'update','Proyek','Website Portofolio','Memperbarui proyek Website Portofolio.','2026-07-18 11:49:20');
/*!40000 ALTER TABLE `activity_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contact_messages`
--

DROP TABLE IF EXISTS `contact_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contact_messages` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `sender_email` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subject` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `delivery_status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'pending',
  `is_read` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  KEY `ix_contact_messages_user_id` (`user_id`),
  KEY `ix_contact_messages_is_read` (`is_read`),
  KEY `ix_contact_messages_created_at` (`created_at`),
  CONSTRAINT `fk_contact_messages_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=30001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contact_messages`
--

LOCK TABLES `contact_messages` WRITE;
/*!40000 ALTER TABLE `contact_messages` DISABLE KEYS */;
INSERT INTO `contact_messages` VALUES (1,1,'Chris Eka','christianoexel@gmail.com','hai','hai ini xander','94e56096-f1ed-4b70-8f92-93b00d4304ef','sent',1,'2026-07-11 10:45:08');
/*!40000 ALTER TABLE `contact_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiences`
--

DROP TABLE IF EXISTS `experiences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiences` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `posisi` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `perusahaan` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `durasi` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `deskripsi` varchar(400) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  KEY `experiences_user_id_idx` (`user_id`),
  CONSTRAINT `experiences_users_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=60001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiences`
--

LOCK TABLES `experiences` WRITE;
/*!40000 ALTER TABLE `experiences` DISABLE KEYS */;
INSERT INTO `experiences` VALUES (1,1,'Web developer','UKSW','Januari 2025 - Februari 2025','membuat web','2026-07-10 07:11:34'),(30001,1,'Web developer','UKSW','Januari 2026 - Februari 2026','Website POS','2026-07-10 07:48:56');
/*!40000 ALTER TABLE `experiences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles`
--

DROP TABLE IF EXISTS `profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `nama_lengkap` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nama_panggilan` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tempat_lahir` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telepon` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `universitas` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fakultas` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `prodi` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `semester` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `alamat` varchar(400) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `foto_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `foto_public_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `about_headline` varchar(180) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `home_headline` varchar(180) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `skills_headline` varchar(180) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `experience_headline` varchar(180) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `projects_headline` varchar(180) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contact_headline` varchar(180) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  UNIQUE KEY `profiles_user_id_uk` (`user_id`),
  CONSTRAINT `profiles_users_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=30001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles`
--

LOCK TABLES `profiles` WRITE;
/*!40000 ALTER TABLE `profiles` DISABLE KEYS */;
INSERT INTO `profiles` VALUES (1,1,'Christiano Alexander','Xander','Surakarta 14 Agustus 2006','2006-08-14','christianoexel@gmail.com','085861872497','UKSW','Fakultas Teknologi Informasi','Sistem Informasi','Semester 4','Jl. Sampangan No.52, Semanggi, Kec. Ps. Kliwon, Kota Surakarta, Jawa Tengah 57191','https://res.cloudinary.com/dtasldt1g/image/upload/v1783763614/portfolio_xander/profile/srwqcfmpdufjfx6ark3o.jpg','portfolio_xander/profile/srwqcfmpdufjfx6ark3o','Mengenal saya dan perjalanan yang sedang saya bangun.','Christiano Alexander','Kemampuan yang terus saya pelajari dan kembangkan.','Pengalaman yang membentuk proses belajar saya.','Proyek yang dibangun dari proses belajar dan eksplorasi.','Mari berdiskusi dan membangun sesuatu yang bermanfaat.');
/*!40000 ALTER TABLE `profiles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `projects`
--

DROP TABLE IF EXISTS `projects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `projects` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `judul` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `deskripsi` varchar(400) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gambar_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `gambar_public_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `link_project` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  KEY `projects_user_id_idx` (`user_id`),
  CONSTRAINT `projects_users_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=170593;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `projects`
--

LOCK TABLES `projects` WRITE;
/*!40000 ALTER TABLE `projects` DISABLE KEYS */;
INSERT INTO `projects` VALUES (60001,1,'Website Portofolio','Website portofolio dinamis berbasis Flask dan TiDB yang menampilkan profil, keahlian, pengalaman, serta proyek. Dilengkapi dashboard admin, upload gambar melalui Cloudinary, pesan kontak, dan tampilan responsif untuk desktop maupun mobile.','https://res.cloudinary.com/dtasldt1g/image/upload/v1784373955/portfolio_xander/projects/niuzpzn7puaagblqooly.jpg','portfolio_xander/projects/niuzpzn7puaagblqooly','https://portfolio-xander-rho.vercel.app','2026-07-18 11:25:56'),(103401,1,'Website Marketplace Jasa','Website Marketplace Jasa ini merupakan platform yang mempertemukan customer dengan freelancer, khususnya untuk kebutuhan jasa di lingkungan kampus, dengan fitur pencarian jasa, pemesanan, pembayaran melalui Midtrans, chat, pemantauan progres, portofolio, ulasan, penarikan pendapatan, serta pengelolaan dan verifikasi oleh admin; sistem ini dibangun menggunakan Laravel, TiDB Cloud, dan Cloudinary ag','https://res.cloudinary.com/dtasldt1g/image/upload/v1784375284/portfolio_xander/projects/tpqysep7lkriaptbbpdu.jpg','portfolio_xander/projects/tpqysep7lkriaptbbpdu','https://tafinal-production.up.railway.app/','2026-07-18 11:48:06');
/*!40000 ALTER TABLE `projects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skills`
--

DROP TABLE IF EXISTS `skills`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skills` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL,
  `nama_skill` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `icon_class` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `persentase` tinyint unsigned NOT NULL DEFAULT '75',
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  KEY `skills_user_id_idx` (`user_id`),
  CONSTRAINT `skills_users_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=120001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skills`
--

LOCK TABLES `skills` WRITE;
/*!40000 ALTER TABLE `skills` DISABLE KEYS */;
INSERT INTO `skills` VALUES (1,1,'Python','code-2',85),(90001,1,'HTML','code-2',85),(90002,1,'Laravel','code-2',80),(90003,1,'SQL','database',75),(90004,1,'VSC','settings-2',90),(90005,1,'REACT JS','panels-top-left',60);
/*!40000 ALTER TABLE `skills` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'admin',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */,
  UNIQUE KEY `users_username_uk` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=30001;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','scrypt:32768:8:1$wXkev98QB8DrRCW0$44401fc72d8f2c53d9a8d1565a09eeef53284772741319eb9e167b48569a1f6095a633d93d88872307e480f9ba532c3789e450017b95eae4ab1d5a7d374c4287','admin','2026-07-10 05:55:10');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-19 18:22:28
