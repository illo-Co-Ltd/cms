-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: localhost    Database: cms
-- ------------------------------------------------------
-- Server version	8.0.22

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
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `id` int NOT NULL AUTO_INCREMENT,
  `model` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `serial` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `owner` int NOT NULL,
  `created` timestamp NULL DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `last_edited` timestamp NULL DEFAULT NULL,
  `edited_by` int DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `device_serial_uindex` (`serial`),
  KEY `device_user_id_fk` (`owner`),
  KEY `device_user_id_fk_2` (`created_by`),
  KEY `device_user_id_fk_3` (`edited_by`),
  CONSTRAINT `device_user_id_fk` FOREIGN KEY (`owner`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `device_user_id_fk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `device_user_id_fk_3` FOREIGN KEY (`edited_by`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='촬영장치정보';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image` (
  `id` int NOT NULL AUTO_INCREMENT,
  `project` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `target` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `path` varchar(260) COLLATE utf8mb4_unicode_ci NOT NULL,
  `device` int NOT NULL,
  `created` timestamp NOT NULL,
  `created_by` int DEFAULT NULL,
  `label` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `offset_x` int NOT NULL,
  `offset_y` int NOT NULL,
  `offset_z` int NOT NULL,
  `pos_x` int NOT NULL,
  `pos_y` int NOT NULL,
  `pos_z` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `image_path_uindex` (`path`),
  KEY `image_device_id_fk` (`device`),
  KEY `image_user_id_fk` (`created_by`),
  CONSTRAINT `image_device_id_fk` FOREIGN KEY (`device`) REFERENCES `device` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `image_user_id_fk` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='이미지 메타데이터';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` timestamp NULL DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `last_edited` timestamp NULL DEFAULT NULL,
  `edited_by` int DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_company_uindex` (`company`),
  UNIQUE KEY `user_username_uindex` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='사용자정보';
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-06  9:37:51
