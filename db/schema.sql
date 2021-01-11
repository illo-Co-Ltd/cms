--
-- Table structure for table `user`
--
#DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `userid` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `username` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `company` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created` timestamp NULL DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `last_edited` timestamp NULL DEFAULT NULL,
  `edited_by` int DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `is_deleted` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_userid_uindex` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='사용자정보';

--
-- Table structure for table `device`
--
#DROP TABLE IF EXISTS `device`;
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

--
-- Table structure for table `image`
--
#DROP TABLE IF EXISTS `image`;
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

-- Dump completed on 2021-01-06  9:37:51
