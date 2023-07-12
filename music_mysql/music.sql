-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: music
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.22.04.2

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
-- Table structure for table `album`
--

DROP TABLE IF EXISTS `album`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `album` (
  `name` varchar(50) NOT NULL,
  `publish_time` date DEFAULT NULL,
  `company` varchar(50) DEFAULT NULL,
  `performer` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `album`
--

LOCK TABLES `album` WRITE;
/*!40000 ALTER TABLE `album` DISABLE KEYS */;
INSERT INTO `album` VALUES ('album1','2002-05-28','company1','A'),('album2','1990-11-12','company1','B'),('album3','2012-07-09','company2','C'),('album4','2018-08-12','company2','D');
/*!40000 ALTER TABLE `album` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `composer`
--

DROP TABLE IF EXISTS `composer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `composer` (
  `name` varchar(50) NOT NULL,
  `birth_time` varchar(50) DEFAULT NULL,
  `death_time` varchar(50) DEFAULT NULL,
  `birthplace` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `composer`
--

LOCK TABLES `composer` WRITE;
/*!40000 ALTER TABLE `composer` DISABLE KEYS */;
--INSERT INTO `composer` VALUES ('Franz Joseph Haydn','31 mar 1732' ,  '31 may 1809' ,'Rohrau' ),('Carl Philipp Emanuel Bach','8 mar 1714 ',  '14 dec 1788' ,'Weimar' ),('Johann Sebastian Bach','31 mar 1685' ,  '28 jul 1750' ,'Eisenach '),('Richard Wagner','22 may 1813' ,  '13 feb 1883' ,'Leipzig');
/*!40000 ALTER TABLE `composer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `info`
--

DROP TABLE IF EXISTS `info`;
/*!50001 DROP VIEW IF EXISTS `info`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `info` AS SELECT 
 1 AS `opus`,
 1 AS `name`,
 1 AS `composer`,
 1 AS `album`,
 1 AS `country`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `piece`
--

DROP TABLE IF EXISTS `piece`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `piece` (
  `Opus` varchar(50) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `composer` varchar(50) NOT NULL,
  `album` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Opus`,`composer`),
  KEY `piece_composer_name_fk` (`composer`),
  KEY `piece_album_name_fk` (`album`),
  CONSTRAINT `piece_album_name_fk` FOREIGN KEY (`album`) REFERENCES `album` (`name`),
  CONSTRAINT `piece_composer_name_fk` FOREIGN KEY (`composer`) REFERENCES `composer` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `piece`
--

LOCK TABLES `piece` WRITE;
/*!40000 ALTER TABLE `piece` DISABLE KEYS */;
--INSERT INTO `piece` VALUES ('Op. 1','Piano Concerto No. 1 in F sharp minor','Rachmaninoff','album3'),('Op. 10, No. 3','Etude in E major','Chopin','album1'),('Op. 23','Piano Concerto No. 1 in B flat minor','Tchaikovsky','album2'),('Op. 25, No. 1','Etude in A flat major ','Chopin','album1'),('Op. 25, No. 12','Etude in C minor ','Chopin','album1'),('Op. 25, No. 9','Etude in G flat major','Chopin','album1'),('Op. 38','Ballade No. 2 in F major','Chopin','album1'),('Op. 43','Rhapsody on a Theme of Paganini','Rachmaninoff','album3'),('Op. 58','Piano Sonata No. 3 in B minor','Chopin','album1'),('Op. 74','Symphony No. 6 in B minor Pathétique','Tchaikovsky','album2'),('Op. 81a','Piano Sonata No. 26 (\"Les Adieux\"), E flat','Beethoven','album4');
/*!40000 ALTER TABLE `piece` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;



/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `check_insert_piece` BEFORE INSERT ON `piece` FOR EACH ROW begin
        if new.composer not in (select name from composer)  then
            signal SQLSTATE '45000'
            set message_text = "composer not exsits.";
        end if;
    end

/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `info`
--

/*!50001 DROP VIEW IF EXISTS `info`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `info` AS select `piece`.`Opus` AS `opus`,`piece`.`name` AS `name`,`piece`.`composer` AS `composer`,`piece`.`album` AS `album`,`composer`.`country` AS `country` from (`piece` join `composer`) where (`piece`.`composer` = `composer`.`name`) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;


create procedure update_album(in opus_name varchar(50), in album_name varchar(50))
begin
    if album_name not in (select name from album) then
        signal sqlstate '45000'
        set message_text = 'album not exists.';
    else
        update piece set album = album_name where Opus like CONCAT('%', opus_name, '%');
    end if;
end;


-- Dump completed on 2023-06-01 19:18:50
